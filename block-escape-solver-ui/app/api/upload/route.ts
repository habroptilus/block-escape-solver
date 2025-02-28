import { NextResponse } from "next/server";

const EXTERNAL_API_URL = process.env.EXTERNAL_API_URL;

if (!EXTERNAL_API_URL) {
  throw new Error("EXTERNAL_API_URL is not defined in environment variables.");
}

export async function POST(request: Request) {
  try {
    const jsonData = await request.json();

    const externalRes = await fetch(`${EXTERNAL_API_URL}/generate-mp4`, {
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
        { error: "Failed to generate video." },
        { status: externalRes.status }
      );
    }

    const headers = new Headers();
    headers.set("Content-Type", "video/mp4");

    return new NextResponse(externalRes.body, { headers });
  } catch (error) {
    console.error("Error in API route:", error);
    return NextResponse.json(
      { error: "Internal Server Error" },
      { status: 500 }
    );
  }
}
