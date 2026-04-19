import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export function PipelinePanel({ input, context, result }) {
  const scoreData = result?.scores
    ? Object.entries(result.scores).map(([key, value]) => ({
        name: key,
        value
      }))
    : [];

  const decisionScoreData = result?.trace?.computed_decision_scores
  ? Object.entries(result.trace.computed_decision_scores).map(([key, value]) => ({
      name: key,
      value
    }))
  : [];

  return (
    <div style={{
      width: "100%",
      padding: 20,
      overflowY: "auto",
      background: "#f7f7f8"
    }}>
      <h2 style={{ marginBottom: 20 }}>Decision System</h2>

      {/* CURRENT INPUT */}
      <div style={cardStyle}>
        <h3>Current Input</h3>
        <div style={codeBlock}>{input || "(typing...)"}</div>
      </div>

      {/* CONTEXT */}
      <div style={cardStyle}>
        <h3>Context Summary</h3>
        <div style={codeBlock}>
          {JSON.stringify(context, null, 2)}
        </div>
      </div>

      <hr style={{
        border: "none",
        borderTop: "1px solid #e5e7eb",
        margin: "16px 0"
      }} />

      {!result && (
        <p style={{ color: "#888", marginTop: 20 }}>
          Waiting for decision...
        </p>
      )}

      {
        result?.error && (
          <p style={{ color: "#888", marginTop: 20 }}>
            Some error happen due to LLM malformed output: {result.error}
          </p>
        )
      }

      {result && !result.error && (
        <>
          {/* INTENT TYPE */}
          <div style={cardStyle}>
            <h3>Intent Type</h3>
            <div>
              {result.classification.intent_type}
            </div>
          </div>

          {/* Issues Discover */}
          <div style={cardStyle}>
            <h3>Issues Discover</h3>
            <div>
              {JSON.stringify(result.classification.issues, null, 2)}
            </div>
          </div>

          {/* KEYWORDS */}
          <div style={cardStyle}>
            <h3>Keywords</h3>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {result.keywords?.map((k, i) => (
                <span key={i} style={tagStyle}>
                  {k}
                </span>
              ))}
            </div>
          </div>

          {/* SCORES CHART */}
          <div style={cardStyle}>
            <h3>Issues/Risks Scores</h3>
            <div style={{ width: "100%", height: 250 }}>
              <ResponsiveContainer>
                <BarChart data={scoreData}>
                  <XAxis dataKey="name" interval={0} tick={{ fontSize: 5 }}  />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* DECISION SCORES CHART */}
          <div style={cardStyle}>
            <h3>Decision Scores</h3>
            <div style={{ width: "100%", height: 250 }}>
              <ResponsiveContainer>
                <BarChart data={decisionScoreData}>
                  <XAxis dataKey="name" interval={0} tick={{ fontSize: 10 }} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* DECISION */}
          <div style={cardStyle}>
            <h3>Decision Results</h3>
            <div style={{
              fontSize: 16,
            }}>
              LLM Decision {result.trace.llm_decision}
            </div>
            <div style={{
              fontSize: 16,
            }}>
              Model Decision {result.trace.computed_decision}
            </div>
            <div style={{
              fontSize: 16,
            }}>
              Model Confidence Score {result.trace.computed_decision_confidence}
            </div>
          </div>

          {/* DECISION */}
          <div style={cardStyle}>
            <h3>System Decision</h3>
            <div style={{
              fontSize: 18,
              fontWeight: "bold",
              color: "#0070f3"
            }}>
              {result.decision}
            </div>
          </div>

          <div style={cardStyle}>
            <h3>Rationale</h3>
            <div >{result.rationale}</div>
          </div>

          {/* UPDATED CONTEXT */}
          <div style={cardStyle}>
            <h3>Updated Context</h3>
            <div style={codeBlock}>
              {JSON.stringify(result.context, null, 2)}
            </div>
          </div>

          {/* REPLY */}
          <div style={cardStyle}>
            <h3>Assistant Reply</h3>
            <div style={codeBlock}>{result.reply}</div>
          </div>

          {/* PROMPTS */}
          <details style={cardStyle}>
            <summary style={{ cursor: "pointer", fontWeight: "bold" }}>
              View LLM Prompts
            </summary>

            <h4>Stage 1</h4>
            <div style={codeBlock}>
              {result.trace?.stage1_prompt}
            </div>

            <h4>Stage 1 Keywords</h4>
            <div style={codeBlock}>
              {result.trace?.stage1_keyword_prompt}
            </div>

            <h4>Stage 3</h4>
            <div style={codeBlock}>
              {result.trace?.stage3_prompt}
            </div>
          </details>

          {/* Responds */}
          <details style={cardStyle}>
            <summary style={{ cursor: "pointer", fontWeight: "bold" }}>
              View LLM Responds
            </summary>

            <h4>Stage 1</h4>
            <div style={codeBlock}>
              {result.trace?.stage1_raw}
            </div>

            <h4>Stage 1 Keywords</h4>
            <div style={codeBlock}>
              {result.trace?.stage1_keyword_raw}
            </div>

            <h4>Stage 3</h4>
            <div style={codeBlock}>
              {result.trace?.stage3_raw}
            </div>
          </details>
        </>
      )}
    </div>
  );
}

const cardStyle = {

  background: "white",

  padding: 16,

  borderRadius: 12,

  marginBottom: 16,

  boxShadow: "0 2px 6px rgba(0,0,0,0.05)"

};

const codeBlock = {

  background: "#111",

  color: "#0f0",

  padding: 12,

  borderRadius: 8,

  fontSize: 12,

  overflowX: "auto",

  whiteSpace: "pre-wrap"

};

const tagStyle = {

  background: "#e0ecff",

  color: "#0366d6",

  padding: "4px 10px",

  borderRadius: 999,

  fontSize: 12

};