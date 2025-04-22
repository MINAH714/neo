

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
}

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('flightSearchForm');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();  // 폼 제출 기본 동작 막기

        const origin = document.getElementById('origin').value;
        const destination = document.getElementById('destination').value;
        const date = document.getElementById('date').value;

        const flightResultDiv = document.getElementById('flightResult');
        flightResultDiv.innerHTML = '<p>가격 분석 중...</p>';

        try {
            const response = await fetch(`http://192.168.1.50:3000/api/total_final/flight_Prices?origin=${origin}&destination=${destination}&departureDate=${date}`);
            const data = await response.json();

            if (!data.Result) {
                throw new Error(data.message || '데이터를 가져오는데 실패했습니다.');
            }

            const realTimePrice = data.real_price;
            const oneYearAgoPrice = data.past_price_metrics["1년 전"]?.MEDIUM;
            const twoYearsAgoPrice = data.past_price_metrics["2년 전"]?.MEDIUM;
            const threeYearsAgoPrice = data.past_price_metrics["3년 전"]?.MEDIUM;
            const analysis = data.analysis;

            const resultHTML = `
                <h3>가격 분석 결과</h3>
                <ul>
                    <li>실시간 가격: ${realTimePrice.toLocaleString()} KRW</li>
                    <li>1년 전 가격: ${oneYearAgoPrice?.toLocaleString() ?? 'N/A'} KRW</li>
                    <li>2년 전 가격: ${twoYearsAgoPrice?.toLocaleString() ?? 'N/A'} KRW</li>
                    <li>3년 전 가격: ${threeYearsAgoPrice?.toLocaleString() ?? 'N/A'} KRW</li>
                </ul>
                <h4>분석</h4>
                <p>${analysis}</p>
            `;

            flightResultDiv.innerHTML = resultHTML;
        } catch (error) {
            flightResultDiv.innerHTML = `<p>오류 발생: ${error.message}</p>`;
        }
    });
});