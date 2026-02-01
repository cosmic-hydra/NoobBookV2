"""
Research Processor - Handles deep research source processing.

Educational Note: This processor orchestrates research using different providers:
1. Claude (default): Uses DeepResearchAgent with web search tool loop
2. Perplexity: Uses Perplexity AI for draft, then Claude cross-check

Processing steps:
1. Reads the research request (.research JSON file)
2. Routes to appropriate provider based on request
3. For Perplexity: draft → cross-check → finalize
4. For Claude: existing agentic loop behavior
5. Saves result, runs embeddings, generates summary
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

from app.utils.text import build_processed_output
from app.utils.path_utils import get_processed_dir, get_chunks_dir
from app.utils.embedding_utils import needs_embedding, count_tokens
from app.services.ai_services.embedding_service import embedding_service
from app.services.ai_services.summary_service import summary_service


def process_research(
    project_id: str,
    source_id: str,
    source: Dict[str, Any],
    raw_file_path: Path,
    source_service
) -> Dict[str, Any]:
    """
    Process a research source by running the deep research agent.

    Educational Note: This is a long-running process that:
    1. Loads the research request parameters
    2. Runs an AI agent with web search capabilities
    3. Compiles findings into a structured document
    4. Embeds the content for RAG retrieval

    Args:
        project_id: The project UUID
        source_id: The source UUID
        source: Source metadata dict
        raw_file_path: Path to the .research JSON file
        source_service: Reference to source_service for updates

    Returns:
        Dict with success status
    """
    processed_dir = get_processed_dir(project_id)
    processed_path = processed_dir / f"{source_id}.txt"

    # Load research request
    with open(raw_file_path, "r", encoding="utf-8") as f:
        research_request = json.load(f)

    topic = research_request.get("topic", "Unknown Topic")
    description = research_request.get("description", "")
    links = research_request.get("links", [])
    provider = research_request.get("provider", "claude")  # Default to Claude

    source_name = source.get("name", topic)

    print(f"Starting research for: {topic}")
    print(f"Provider: {provider}")
    print(f"Description: {description[:100]}...")
    print(f"Reference links: {len(links)}")

    try:
        # Route to appropriate research method based on provider
        if provider == "perplexity":
            research_result = _research_with_perplexity(
                project_id=project_id,
                source_id=source_id,
                topic=topic,
                description=description,
                links=links,
                processed_path=processed_path
            )
        else:
            # Default to Claude DeepResearchAgent
            research_result = _research_with_claude(
                project_id=project_id,
                source_id=source_id,
                topic=topic,
                description=description,
                links=links,
                processed_path=processed_path
            )

        if not research_result.get("success"):
            raise Exception(research_result.get("error", "Research failed"))

        # Read the content that the agent wrote to file
        if not processed_path.exists():
            raise Exception("Research agent did not create output file")

        with open(processed_path, "r", encoding="utf-8") as f:
            research_content = f.read()

        if not research_content:
            raise Exception("Research agent wrote empty content")

        segments_written = research_result.get("segments_written", 0)
        iterations = research_result.get("iterations", 0)
        print(f"Research complete: {len(research_content)} chars, {segments_written} segments, {iterations} iterations")

    except Exception as e:
        print(f"Research agent error: {e}")
        source_service.update_source(
            project_id,
            source_id,
            status="error",
            processing_info={
                "error": str(e),
                "processor": "research_processor"
            }
        )
        return {"success": False, "error": str(e)}

    # Calculate token count for metadata
    token_count = count_tokens(research_content)

    # Build metadata for RESEARCH type
    metadata = {
        "topic": topic,
        "link_count": len(links),
        "character_count": len(research_content),
        "token_count": token_count
    }

    # Use centralized build_processed_output for consistent format
    # Research output is treated as a single "page" document
    processed_content = build_processed_output(
        pages=[research_content],
        source_type="RESEARCH",
        source_name=source_name,
        metadata=metadata
    )

    # Save processed content
    with open(processed_path, "w", encoding="utf-8") as f:
        f.write(processed_content)

    processing_info = {
        "processor": "research_processor",
        "topic": topic,
        "link_count": len(links),
        "character_count": len(research_content),
        "token_count": token_count,
        "total_pages": 1,
        "segments_written": segments_written,
        "iterations": iterations,
        "researched_at": datetime.now().isoformat()
    }

    # Process embeddings
    embedding_info = _process_embeddings(
        project_id=project_id,
        source_id=source_id,
        source_name=source_name,
        processed_text=processed_content,
        source_service=source_service
    )

    # Generate summary after embeddings
    source_metadata = {**source, "processing_info": processing_info, "embedding_info": embedding_info}
    summary_info = _generate_summary(project_id, source_id, source_metadata)

    source_service.update_source(
        project_id,
        source_id,
        status="ready",
        active=True,  # Auto-activate when ready
        processing_info=processing_info,
        embedding_info=embedding_info,
        summary_info=summary_info if summary_info else None
    )

    print(f"Research source ready: {source_name}")
    return {"success": True, "status": "ready"}


def _process_embeddings(
    project_id: str,
    source_id: str,
    source_name: str,
    processed_text: str,
    source_service
) -> Dict[str, Any]:
    """
    Process embeddings for a research source.

    Educational Note: Research documents are typically comprehensive and
    benefit greatly from semantic search via embeddings.
    """
    try:
        # Get embedding info
        _, token_count, reason = needs_embedding(text=processed_text)

        # Update status to "embedding" before starting
        source_service.update_source(project_id, source_id, status="embedding")
        print(f"Starting embedding for research: {source_name} ({reason})")

        # Process embeddings using the embedding service
        chunks_dir = get_chunks_dir(project_id)
        return embedding_service.process_embeddings(
            project_id=project_id,
            source_id=source_id,
            source_name=source_name,
            processed_text=processed_text,
            chunks_dir=chunks_dir
        )

    except Exception as e:
        print(f"Error processing embeddings for research {source_id}: {e}")
        return {
            "is_embedded": False,
            "embedded_at": None,
            "token_count": 0,
            "chunk_count": 0,
            "reason": f"Embedding error: {str(e)}"
        }


def _generate_summary(
    project_id: str,
    source_id: str,
    source_metadata: Dict[str, Any]
) -> Dict[str, Any]:
    """Generate a summary for a processed research source."""
    try:
        print(f"Generating summary for research source: {source_id}")
        result = summary_service.generate_summary(
            project_id=project_id,
            source_id=source_id,
            source_metadata=source_metadata
        )
        if result:
            print(f"Summary generated for research {source_id}: {len(result.get('summary', ''))} chars")
            return result
        return {}
    except Exception as e:
        print(f"Error generating summary for research {source_id}: {e}")
        return {}


def _research_with_claude(
    project_id: str,
    source_id: str,
    topic: str,
    description: str,
    links: List[str],
    processed_path: Path
) -> Dict[str, Any]:
    """
    Execute research using Claude's DeepResearchAgent.

    Educational Note: This is the original research method using
    Claude's agentic loop with web search tools.

    Args:
        project_id: Project UUID
        source_id: Source UUID
        topic: Research topic
        description: Research focus
        links: Reference URLs
        processed_path: Path to write output

    Returns:
        Dict with success status and metadata
    """
    from app.services.ai_agents.deep_research_agent import deep_research_agent

    print("[Claude] Running DeepResearchAgent")
    
    return deep_research_agent.research(
        project_id=project_id,
        source_id=source_id,
        topic=topic,
        description=description,
        links=links,
        output_path=str(processed_path)
    )


def _research_with_perplexity(
    project_id: str,
    source_id: str,
    topic: str,
    description: str,
    links: List[str],
    processed_path: Path
) -> Dict[str, Any]:
    """
    Execute research using Perplexity with Claude cross-check.

    Educational Note: This two-step process:
    1. Perplexity generates draft research with citations
    2. Claude reviews and improves the draft

    Args:
        project_id: Project UUID
        source_id: Source UUID
        topic: Research topic
        description: Research focus
        links: Reference URLs
        processed_path: Path to write output

    Returns:
        Dict with success status and metadata
    """
    from app.services.integrations.perplexity import perplexity_service
    from app.services.ai_services.crosscheck_service import crosscheck_service

    print("[Perplexity] Step 1: Generating draft research")
    
    # Step 1: Get draft from Perplexity
    perplexity_result = perplexity_service.research(
        topic=topic,
        description=description,
        links=links
    )

    if not perplexity_result.get("success"):
        error = perplexity_result.get("error", "Perplexity research failed")
        raise Exception(error)

    draft_content = perplexity_result.get("content", "")
    citations = perplexity_result.get("citations", [])
    perplexity_usage = perplexity_result.get("usage", {})

    print(f"[Perplexity] Draft complete: {len(draft_content)} chars, {len(citations)} citations")

    # Step 2: Cross-check with Claude
    print("[Claude] Step 2: Cross-checking and improving draft")
    
    crosscheck_result = crosscheck_service.crosscheck_research(
        draft_content=draft_content,
        topic=topic,
        description=description,
        links=links,
        citations=citations,
        project_id=project_id
    )

    if not crosscheck_result.get("success"):
        error = crosscheck_result.get("error", "Cross-check failed")
        raise Exception(error)

    final_content = crosscheck_result.get("content", "")
    claude_usage = crosscheck_result.get("usage", {})

    print(f"[Claude] Cross-check complete: {len(final_content)} chars")

    # Write final content to file
    with open(processed_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    # Return result in standard format
    return {
        "success": True,
        "output_path": str(processed_path),
        "segments_written": 1,  # Single segment for Perplexity
        "iterations": 2,  # Perplexity + Claude crosscheck
        "usage": {
            "perplexity": perplexity_usage,
            "claude": claude_usage
        },
        "citations": citations
    }

