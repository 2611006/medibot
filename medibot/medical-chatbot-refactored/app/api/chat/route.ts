import { LangChainStream, StreamingTextResponse } from "ai";
import { ChatOpenAI } from "langchain/chat_models/openai";
import { HumanMessage } from "langchain/schema";

export const runtime = "edge";

export async function POST(req: Request) {
  const { messages } = await req.json();

  const llm = new ChatOpenAI({
    modelName: "gpt-4o-mini",
    temperature: 0.3,
    apiKey: process.env.OPENAI_API_KEY,
  });

  const stream = await LangChainStream(llm, {
    messages: messages.map(
      (m: any) => new HumanMessage(m.content)
    ),
  });

  return new StreamingTextResponse(stream);
}

