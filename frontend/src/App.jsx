import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

export default function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const runResearch = async () => {
    if (!question.trim()) return;

    setLoading(true);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/api/v1/research",
        {
          question,
          max_retries: 1,
          timeout_seconds: 300,
        }
      );

      setResult(response.data);
    } catch (error) {
      console.error(error);
      alert("Unable to connect to the backend.");
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 text-black flex justify-center px-8 py-12">
      <div className="w-full max-w-6xl">

        <h1 className="text-5xl font-bold tracking-tight">
          Research Agent
        </h1>

        <p className="mt-4 text-lg text-gray-600">
          Multi-Agent AI Research Assistant powered by LangGraph and NVIDIA Foundation Models.
        </p>

        <div className="mt-10">
          <textarea
            className="w-full h-40 rounded-2xl border border-gray-300 bg-white p-5 text-lg outline-none focus:ring-2 focus:ring-black"
            placeholder="Ask any research question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />

          <button
            onClick={runResearch}
            className="mt-6 rounded-xl bg-black text-white px-8 py-3 hover:bg-gray-800 transition"
          >
            {loading ? "Researching..." : "Start Research"}
          </button>
        </div>

        {loading && (
          <div className="mt-8 rounded-2xl border bg-white p-6 shadow-sm">
            <p className="text-lg font-semibold">
              Running Research...
            </p>

            <p className="text-gray-500 mt-2">
              Planner → Tool Executor → Writer → Critic
            </p>
          </div>
        )}

        {result && (
          <>
            <div className="mt-14">

              <div className="bg-white rounded-3xl border shadow-sm p-10">

                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  rehypePlugins={[rehypeRaw]}
                  components={{
                    h1: ({ children }) => (
                      <h1 className="text-5xl font-bold mb-8 mt-2">
                        {children}
                      </h1>
                    ),

                    h2: ({ children }) => (
                      <h2 className="text-3xl font-bold mt-12 mb-6 border-b pb-3">
                        {children}
                      </h2>
                    ),

                    h3: ({ children }) => (
                      <h3 className="text-2xl font-semibold mt-8 mb-4">
                        {children}
                      </h3>
                    ),

                    p: ({ children }) => (
                      <p className="text-[17px] leading-8 text-gray-800 mb-5">
                        {children}
                      </p>
                    ),

                    ul: ({ children }) => (
                      <ul className="list-disc pl-8 space-y-3 mb-6">
                        {children}
                      </ul>
                    ),

                    ol: ({ children }) => (
                      <ol className="list-decimal pl-8 space-y-3 mb-6">
                        {children}
                      </ol>
                    ),

                    li: ({ children }) => (
                      <li className="leading-8">
                        {children}
                      </li>
                    ),

                    strong: ({ children }) => (
                      <strong className="font-bold text-black">
                        {children}
                      </strong>
                    ),

                    table: ({ children }) => (
                      <div className="overflow-x-auto my-8">
                        <table className="w-full border border-gray-300 rounded-lg overflow-hidden">
                          {children}
                        </table>
                      </div>
                    ),

                    th: ({ children }) => (
                      <th className="border border-gray-300 bg-gray-100 p-4 text-left font-semibold">
                        {children}
                      </th>
                    ),

                    td: ({ children }) => (
                      <td className="border border-gray-300 p-4 align-top">
                        {children}
                      </td>
                    ),

                    code: ({ children }) => (
                      <code className="bg-gray-100 rounded px-2 py-1 text-sm">
                        {children}
                      </code>
                    ),

                    blockquote: ({ children }) => (
                      <blockquote className="border-l-4 border-gray-300 pl-5 italic my-6 text-gray-700">
                        {children}
                      </blockquote>
                    ),
                  }}
                >
                  {result.final_answer}
                </ReactMarkdown>

              </div>

            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-10">

              <div className="rounded-2xl border bg-white p-6 shadow-sm">
                <p className="text-gray-500 text-sm">
                  Duration
                </p>

                <h3 className="text-2xl font-bold mt-2">
                  {result.execution_metrics.total_duration.toFixed(2)} s
                </h3>
              </div>

              <div className="rounded-2xl border bg-white p-6 shadow-sm">
                <p className="text-gray-500 text-sm">
                  Tool Calls
                </p>

                <h3 className="text-2xl font-bold mt-2">
                  {result.execution_metrics.tool_calls}
                </h3>
              </div>

              <div className="rounded-2xl border bg-white p-6 shadow-sm">
                <p className="text-gray-500 text-sm">
                  Critic
                </p>

                <h3 className="text-2xl font-bold mt-2">
                  {result.critic_feedback.status}
                </h3>
              </div>

              <div className="rounded-2xl border bg-white p-6 shadow-sm">
                <p className="text-gray-500 text-sm">
                  Retries
                </p>

                <h3 className="text-2xl font-bold mt-2">
                  {result.execution_metrics.retry_count}
                </h3>
              </div>

            </div>
          </>
        )}
      </div>
    </div>
  );
}