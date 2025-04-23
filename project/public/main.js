function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
}

document.getElementById("flightSearchForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const originLeft =document.querySelector(".left-origin");
    originLeft.classList.add("noshow")

    const origin = document.getElementById("origin").value;
    const destination = document.getElementById("destination").value;
    const date = document.getElementById("date").value;

    const response = await fetch(`/api/flight_analysis?origin=${origin}&destination=${destination}&departureDate=${date}`);
    const data = await response.json();

    const analysisText = data.analysis;
    const prices = data.prices;

    // 왼쪽 문구 숨기기 & 분석 결과 보이기
    document.getElementById("flight-title").style.display = "none";
    document.getElementById("flight-analysis-result").style.display = "block";
    document.getElementById("flight-analysis-text").innerText = analysisText;

    // 그래프 그리기
    fetchFlightData(data);
});

function fetchFlightData(data) {
        if (window.flightChart) {
        window.flightChart.destroy();
    }
  
    if (data.Result) {
      const labels = Object.keys(data.simulated_past_prices); // ["1년 전", "2년 전", "3년 전"]
      const pastPrices = Object.values(data.simulated_past_prices); // [113195.6, 146034.33, 187977.38]
      const realPrice = data.real_price;
      const avgPrice = data.average_simulated_price;
  
      const ctx = document.getElementById('flight-chart').getContext('2d');
      window.flightChart=new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [
            {
                label: '현재 항공권 가격',
                data: [realPrice, realPrice, realPrice],
                type: 'line',
                borderColor: 'rgb(249, 56, 39)',
                borderWidth: 2,
                fill: false,
                pointRadius: 4,
                tension: 0
            },
            {
                label: '과거 평균 가격',
                data: [avgPrice, avgPrice, avgPrice],
                type: 'line',
                borderColor: 'rgb(255, 169, 85)',
                borderDash: [5, 5],
                borderWidth: 2,
                fill: false,
                pointRadius: 0,
                tension: 0
            },
            {
                label: '과거 항공권 가격',
                data: pastPrices,
                backgroundColor: 'rgb(122, 198, 210)'
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: '과거 3년간 항공권 가격 vs 현재 가격'
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              ticks: {
                callback: value => value.toLocaleString() + '원'
              }
            }
          }
        }
      });
    } else {
      console.error(result.message);
    }
  }
  
  

// // ✨ Chart.js로 그래프 그리는 함수
// function renderFlightChart(prices) {
//     const ctx = document.getElementById('flight-chart').getContext('2d');

//     // 기존 차트 있으면 제거
//     if (window.flightChart) {
//         window.flightChart.destroy();
//     }

//     window.flightChart = new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: Object.keys(prices),
//             datasets: [{
//                 label: '항공권 평균 가격',
//                 data: Object.values(prices),
//                 backgroundColor: ['#aad3df', '#85b3d1', '#5c95c2', '#3c78b3']
//             }]
//         },
//         options: {
//             scales: {
//                 y: {
//                     beginAtZero: false
//                 }
//             }
//         }
//     });
// }
