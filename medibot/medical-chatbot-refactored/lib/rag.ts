import { ChatOpenAI } from "@langchain/openai";
import { MemoryVectorStore } from "@langchain/community/vectorstores/memory";
import { OpenAIEmbeddings } from "@langchain/openai";

const llm = new ChatOpenAI({
  model: "gpt-4o-mini",
  temperature: 0.3
});

const embeddings = new OpenAIEmbeddings();

const vectorStore = await MemoryVectorStore.fromTexts(
  [
    "Diabetes is a chronic condition where blood sugar levels are too high.",
    "Type 1 diabetes is autoimmune.",
    "Type 2 diabetes is related to insulin resistance."
  ],
  [{ source: "medical" }],
  embeddings
);

export async function askMedibot(question: string) {
  const docs = await vectorStore.similaritySearch(question, 3);

  const context = docs.map(d => d.pageContent).join("\n");

  const response = await llm.invoke(
    `Answer medically using this context:\n${context}\n\nQuestion: ${question}`
  );

  return response.content;
}
