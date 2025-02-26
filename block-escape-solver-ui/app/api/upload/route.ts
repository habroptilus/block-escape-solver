import { NextResponse } from "next/server";

const EXTERNAL_API_URL = process.env.EXTERNAL_API_URL;

if (!EXTERNAL_API_URL) {
  throw new Error("EXTERNAL_API_URL is not defined in environment variables.");
}

export async function POST(request: Request) {
  try {
    const jsonData = await request.json();

    const externalRes = await fetch(`${EXTERNAL_API_URL}/generate-gif`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(jsonData),
    });

    if (externalRes.status === 400) {
      return NextResponse.json(
        { error: "Invalid board configuration: No possible solution." },
        { status: 400 }
      );
    }

    if (!externalRes.ok) {
      return NextResponse.json(
        { error: "Failed to generate GIF." },
        { status: externalRes.status }
      );
    }

    const arrayBuffer = await externalRes.arrayBuffer();
    const headers = new Headers();
    headers.set("Content-Type", "image/gif");

    return new NextResponse(Buffer.from(arrayBuffer), { headers });
  } catch (error) {
    console.error("Error in API route:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
