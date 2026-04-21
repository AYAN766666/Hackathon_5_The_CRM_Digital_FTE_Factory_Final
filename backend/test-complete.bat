@echo off
REM ================================================
REM Complete API Test with Ticket Status
REM ================================================

cd /d "%~dp0"

echo.
echo ================================================
echo   Customer Success FTE - Complete API Test
echo ================================================
echo.

echo [TEST 1] Health Check...
echo ----------------------------------------
curl -s http://localhost:8000/health
echo.
echo.

echo [TEST 2] Create Support Ticket...
echo ----------------------------------------
echo Creating ticket...
python -c "import httpx; r=httpx.post('http://localhost:8000/support/submit', json={'name':'Test','email':'test@test.com','category':'General','message':'Test message for API testing with enough characters'}, timeout=30.0); print(r.text)"
echo.
echo.

echo [TEST 3] Get Ticket Status...
echo ----------------------------------------
echo Use the ticket ID from above to test:
echo curl http://localhost:8000/support/ticket/YOUR_TICKET_ID
echo.

echo ================================================
echo   Manual Test Instructions:
echo ================================================
echo.
echo 1. Open browser: http://localhost:8000/docs
echo 2. Click on POST /support/submit
echo 3. Click "Try it out"
echo 4. Fill in the form and execute
echo 5. Copy the ticket_id from response
echo 6. Click on GET /support/ticket/{ticket_id}
echo 7. Click "Try it out"
echo 8. Paste ticket_id and execute
echo 9. You should see the conversation!
echo.

pause
