import { askMedibot } from "@/lib/rag";

export async function POST(req: Request) {
  const { question } = await req.json();
  const answer = await askMedibot(question);

  return Response.json({ answer });
}
