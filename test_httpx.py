import httpx

url = "https://67fd5940-5458-43f8-b984-d01e98330496.australia-southeast1-0.gcp.cloud.qdrant.io"

headers = {
    "api-key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIiwic3ViamVjdCI6ImFwaS1rZXk6Y2UzYzAzMTQtMmIxZS00Yjk2LTk5NzItYjhmN2FjNTUwNDk5In0.geRKGASeJIHXVrpQ350YWzGDcGlUFjTOjEwGC3r1bhk"
}

print("Sending request...")

r = httpx.get(
    url + "/collections",
    headers=headers,
    timeout=30,
)

print(r.status_code)
print(r.text)