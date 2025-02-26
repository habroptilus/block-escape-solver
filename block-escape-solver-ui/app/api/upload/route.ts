import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    // クライアントから送られた JSON データを取得
    const jsonData = await request.json();

    // 外部エンドポイント へ JSON を POST
    const externalRes = await fetch("http://127.0.0.1:8000/generate-gif", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(jsonData),
    });

    if (externalRes.status === 400) {
      // 400エラーの場合は適切なメッセージを返す
      return NextResponse.json(
        { error: "Invalid board configuration: No possible solution." },
        { status: 400 }
      );
    }

    if (!externalRes.ok) {
      // その他のエラー
      return NextResponse.json(
        { error: "Failed to generate GIF." },
        { status: externalRes.status }
      );
    }

    // GIF ファイルのバイナリデータを取得
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
