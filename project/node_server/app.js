const express = require("express");
const axios = require("axios");
const path = require("path");
const cors = require("cors");
const app = express();

app.use(express.static(path.resolve(__dirname, '../public')));

app.use(cors());
const PORT = 8000;

app.use(express.json());

app.get("/", (req, res) => {
    res.send("서버 켜짐!");
});

app.get('/api/flight_analysis', async (req, res) => {
  const { origin = 'ICN', destination, departureDate, currency = 'KRW' } = req.query;

  if (!origin || !destination || !departureDate) {
      return res.status(400).json({
          Result: false,
          message: "필수 파라미터가 누락되었습니다."
      });
  }

  try {
      const response = await axios.get('http://192.168.1.50:3000/api/noise/flight_Prices', {
          params: { origin, destination, departureDate, currency },
      });

      res.json(response.data);
  } catch (error) {
      console.error("FastAPI 요청 오류:", error.response?.data || error.message);
      res.status(500).json({
          Result: false,
          message: "FastAPI 서버 요청 중 오류 발생",
          error: error.response?.data || error.message
      });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://192.168.1.50:${PORT}`);
});