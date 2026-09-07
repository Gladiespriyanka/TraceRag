import { useMemo } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  type Node,
  type Edge,
} from "@xyflow/react";

import "@xyflow/react/dist/style.css";

import type { Source } from "../api";

interface EvidenceGraphProps {
  sources: Source[];
}

export default function EvidenceGraph({
  sources,
}: EvidenceGraphProps) {
  const { nodes, edges } = useMemo(() => {

    if (!sources.length) {
      return {
        nodes: [],
        edges: [],
      };
    }

    // -------------------------------------------------------
    // Group retrieved chunks by document
    // -------------------------------------------------------

    const grouped = new Map<string, Source[]>();

    for (const source of sources) {

      if (!grouped.has(source.document_id)) {
        grouped.set(source.document_id, []);
      }

      grouped.get(source.document_id)!.push(source);
    }

    const nodes: Node[] = [];
    const edges: Edge[] = [];

    let documentIndex = 0;

    // -------------------------------------------------------
    // Create Document → Chunk graph
    // -------------------------------------------------------

    for (const [documentId, documentSources] of grouped) {

      const document = documentSources[0];

      const documentNodeId = `document-${documentId}`;

      // Document node
      nodes.push({
        id: documentNodeId,

        position: {
          x: documentIndex * 420,
          y: 40,
        },

        data: {
          label: (
            <div className="evidence-document-node">
              <div className="graph-node-type">
                DOCUMENT
              </div>

              <strong>
                {document.filename}
              </strong>

              <small>
                {documentSources.length} retrieved chunk
                {documentSources.length !== 1 ? "s" : ""}
              </small>
            </div>
          ),
        },

        style: {
          width: 280,
          borderRadius: 14,
          padding: 14,
          border: "1px solid #9cff2f",
          background: "#10151d",
          color: "#ffffff",
        },
      });

      // -----------------------------------------------------
      // Create chunk nodes
      // -----------------------------------------------------

      documentSources.forEach((source, index) => {

        const chunkNodeId = `chunk-${source.chunk_id}`;

        const preview =
          source.content.length > 180
            ? `${source.content.slice(0, 180)}...`
            : source.content;

        nodes.push({
          id: chunkNodeId,

          position: {
            x: documentIndex * 420,
            y: 180 + index * 170,
          },

          data: {
            label: (
              <div className="evidence-chunk-node">

                <div className="graph-node-header">
                  <span className="graph-node-type">
                    EVIDENCE CHUNK
                  </span>

                  <span className="graph-rank">
                    #{index + 1}
                  </span>
                </div>

                <div className="graph-preview">
                  {preview}
                </div>

                <div className="graph-score">
                  Retrieval:{" "}
                  {source.retrieval_score.toFixed(4)}
                  {" • "}
                  Rerank:{" "}
                  {source.rerank_score.toFixed(3)}
                </div>

              </div>
            ),
          },

          style: {
            width: 320,
            borderRadius: 12,
            padding: 14,
            border: "1px solid #293342",
            background: "#0d1219",
            color: "#dbe4f0",
          },
        });

        // ---------------------------------------------------
        // REAL relationship:
        //
        // Document contains this chunk
        // ---------------------------------------------------

        edges.push({
          id: `edge-${documentId}-${source.chunk_id}`,

          source: documentNodeId,
          target: chunkNodeId,

          label: "contains",

          animated: false,

          style: {
            strokeWidth: 1.5,
          },

          labelStyle: {
            fontSize: 11,
          },
        });
      });

      documentIndex++;
    }

    return {
      nodes,
      edges,
    };

  }, [sources]);

  // ---------------------------------------------------------
  // Empty state
  // ---------------------------------------------------------

  if (!sources.length) {
    return (
      <div className="empty">
        Run a query to build the evidence graph.
      </div>
    );
  }

  // ---------------------------------------------------------
  // Graph
  // ---------------------------------------------------------

  return (
    <div
      className="graph"
      style={{
        width: "100%",
        height: "650px",
      }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
        fitViewOptions={{
          padding: 0.2,
        }}
      >
        <Background />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}