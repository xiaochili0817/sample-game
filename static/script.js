const socket = io();
const yourChoiceElement = document.getElementById('your-choice');
const opponentChoiceElement = document.getElementById('opponent-choice');
const resultTextElement = document.getElementById('resultText');

function joinGame() {
    const username = document.getElementById('username').value;
    const room = document.getElementById('room').value;
    socket.emit('join', {username: username, room: room});

    document.getElementById('waiting').style.display = 'block';
    document.getElementById('choices').style.display = 'none';
}

socket.on('player_joined', data => {
    if (data.players.length === 2) {
        document.getElementById('waiting').style.display = 'none';
        document.getElementById('choices').style.display = 'block';
    }
});

function makeChoice(choice) {
    socket.emit('make_choice', {choice: choice});
    document.getElementById('choices').style.display = 'none';

    // 显示玩家的选择
    yourChoiceElement.src = `static/${choice}.png`;
    document.getElementById('result').style.display = 'block';

    // 开始对手选择的动画
    startOpponentAnimation();
}

function startOpponentAnimation() {
    const choices = ['rock', 'paper', 'scissors'];
    let index = 0;
    opponentChoiceElement.src = `static/${choices[index]}.png`;

    const intervalId = setInterval(() => {
        index = (index + 1) % choices.length;
        opponentChoiceElement.src = `static/${choices[index]}.png`;
    }, 100);

    // 等待服务器返回结果
    socket.on('result', data => {
        clearInterval(intervalId);  // 停止动画
        opponentChoiceElement.src = `static/${data.choice2}.png`;  // 显示对手的最终选择
        resultTextElement.textContent = `${data.player1} chose ${data.choice1}, ${data.player2} chose ${data.choice2}. ${data.result}`;
    });
}

