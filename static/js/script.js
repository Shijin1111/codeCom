var parts = [];
var waves = []
var can = document.getElementById("cs");
var ctx = can.getContext("2d");
can.width = window.innerWidth;
can.height = window.innerHeight;

function randFrom(min, max) {
    return Math.random() * (max - min) + min;
}

function randBet(c1, c2) {
    var nArr = [c1, c2];
    return nArr[Math.floor(Math.random() * 2)];
}

function Wave(period, amp, waveL, dir) {
    this.phase = 0;
    var dirVal = (dir === "left") ? 1 : -1;

    this.applyTo = function(points) {
        for (var i = 0; i < points.length; i++) {
            var initPhase = 2 * Math.PI * points[i].x / waveL;
            points[i].y += amp * Math.sin(this.phase + (initPhase * dirVal));
            var yVal = amp * Math.sin(this.phase + (initPhase * dirVal));
            var angVel = 2 * Math.PI / period;
            points[i].acc += -(angVel ** 2) * yVal;
        }
        this.phase += 2 * Math.PI / period;
    }
}

function particle(x) {
    this.x = x;
    this.y = 0;
    this.acc = 0;
    this.upd = function() {
        ctx.strokeStyle = "hsl(280,100%," + (Math.abs(this.acc * 60) + 30) + "%)";
        ctx.beginPath();
        ctx.arc(this.x, can.height / 2 + this.y, 10, 0, 2 * Math.PI);
        ctx.stroke();
        this.y = 0;
        this.acc = 0;
    }
}

function gameMake() {
    var num = 400;
    for (var i = 0; i < num; i++) {
        parts.push(new particle(i / (num - 1) * can.width));
    }
    var waveNum = 8;
    for (var i = 0; i < waveNum; i++) {
        waves.push(new Wave(randFrom(50, 120), can.height / (2 * waveNum), randFrom(200, can.width), randBet("left", "right")));
    }
}

function gameMove() {
    requestAnimationFrame(gameMove);
    ctx.clearRect(0, 0, can.width, can.height);
    for (var i = 0; i < waves.length; i++) {
        waves[i].applyTo(parts);
    }
    for (var i = 0; i < parts.length; i++) {
        parts[i].upd();
    }
}

gameMake();
gameMove();

window.addEventListener('resize', function() {
    can.width = window.innerWidth;
    can.height = window.innerHeight;
});
