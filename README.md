# 1. Health check

curl http://localhost:8000/health

# 2. Register user

curl -X POST http://localhost:8000/api/v1/auth/register \
 -H "Content-Type: application/json" \
 -d '{"email":"interview@test.com","password":"123456","confirm_password":"123456"}'

# 3. Login

TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
 -H "Content-Type: application/json" \
 -d '{"email":"interview@test.com","password":"123456"}' \
 | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))")

# 4. Create a robot

curl -X POST http://localhost:8000/api/v1/robots/ \
 -H "Authorization: Bearer $TOKEN" \
 -H "Content-Type: application/json" \
 -d '{"name":"Robot T4","serial_number":"T4-001","robot_type":"T4","capabilities":"tap,chip,swipe"}'

# 5. List robots

curl -X GET http://localhost:8000/api/v1/robots/ \
 -H "Authorization: Bearer $TOKEN"

# 6. Test McDonald's terminal

curl http://localhost:8000/api/v1/terminals/mcdonalds

# 7. Simulate payment

curl -X POST http://localhost:8000/api/v1/terminals/test \
 -H "Content-Type: application/json" \
 -d '{"terminal_id":101,"amount":12.95,"payment_method":"tap"}'

# 8. Show API documentation

echo "Open http://localhost:8000/docs in your browser"
