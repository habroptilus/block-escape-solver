import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    // クライアントから送られた JSON データを取得
    const jsonData = await request.json();

    // 外部エンドポイント へJSON を POST
    const externalRes = await fetch("http://127.0.0.1:8000/generate-gif", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(jsonData),
    });

    if (!externalRes.ok) {
      return NextResponse.error();
    }

    // GIF ファイルのバイナリデータを取得
    const arrayBuffer = await externalRes.arrayBuffer();
    const headers = new Headers();
    headers.set("Content-Type", "image/gif");
    return new NextResponse(Buffer.from(arrayBuffer), { headers });
  } catch (error) {
    console.error("Error in API route:", error);
    return NextResponse.error();
  }
}
