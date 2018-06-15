"# BlockChain-Python" 


python app.py -p 5000
python app.py -p 5001

curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/register-node -d "{\"address\": \"http://127.0.0.1:5001\"}"
curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5001/register-node -d "{\"address\": \"http://127.0.0.1:5000\"}"

curl "http://127.0.0.1:5000/chain"
curl "http://127.0.0.1:5001/chain"

curl -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/create-transaction -d "{\"sender\": \"DataProducer\", \"recipient\": \"DataOwner\", \"sensor\": 13}"

curl "http://127.0.0.1:5000/mine"
curl "http://127.0.0.1:5000/chain"

curl "http://127.0.0.1:5000/sync-chain"
curl "http://127.0.0.1:5001/sync-chain"
