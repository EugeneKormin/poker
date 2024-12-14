document.addEventListener("DOMContentLoaded", function() {
    const eventSource = new EventSource('http://103.90.73.217:8001/stream');

    eventSource.onopen = function() {
        console.log("Connection to server opened.");
        document.getElementById('updates').innerText = "Connected to server.";
    };

    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        console.log("Raw data received:", event.data);
        console.log("Parsed data:", data);

        const updatesDiv = document.getElementById('updates');

        if (updatesDiv) {
            updatesDiv.innerHTML = ""; // Очистка предыдущего содержимого

            // Итерация по каждому игроку
            for (let player = 1; player <= 6; player++) {
                const playerData = data[player] || { pot: '-', bet: '-', cards: []}; // Защита от отсутствующих данных
                const isInGame = playerData.in_game;
                const potValue = playerData.pot !== '-' ? playerData.pot : 'Выбыл';
                const betValue = playerData.bet !== '-' ? playerData.bet : 'Выбыл';
                const playerPosition = playerData.my_position !== '-' ? playerData.my_position : '--';
                
                
                // Создание нового div для каждого игрока
                const playerDiv = document.createElement('div');
                playerDiv.className = 'player-update';

                playerDiv.innerHTML = `
                    <p>Игрок ${player}${playerPosition} - Пот: $${potValue}</p>
                    <p>Игрок ${player}${playerPosition} - Текущая ставка: $${betValue}</p>
                    <p>Игрок ${player}${playerPosition} - Карты: ${playerData.cards.length > 0 ?
 playerData.cards.join(', ') : 'Нет'}</p>
                    <p>Игрок ${player}${playerPosition} - В игре: ${isInGame}</p>
                `;

                // Добавление div игрока в обновления
                updatesDiv.appendChild(playerDiv);
            }

            // Отображение информации о доске
            if (data.board && typeof data.board === 'object') {
                const boardDiv = document.createElement('div');
                boardDiv.className = 'board-update';

                // Добавление информации о картах на доске и других элементах
                boardDiv.innerHTML = `
                    <p>Карты на доске: ${data.board.cards.length > 0 ? data.board.cards.join(', ') : 'Нет'}</p>
                    <p>Принятая ставка: $${data.board.accepted_bet}</p>
                    <p>Не принятая ставка: $${data.board.not_accepted_bet}</p>
                    <p>Позиция дилера: Игрок ${data.board.dealer_position}</p>
                    <p>Моя позиция: ${data.board.my_position}
                `;
                
                updatesDiv.appendChild(boardDiv);
            }
        } else {
            console.error("Элемент с ID 'updates' не найден.");
        }
    };

    eventSource.onerror = function(err) {
        console.error("EventSource failed:", err);
        document.getElementById('updates').innerText = "Ошибка подключения к серверу.";
    };
});

