// JavaScript function to generate 6 random unique values in order and populate form
function luckyDip() {

    // create empty set
    let draw = new Set();

    // COMMENT
    let randomBuffer = new Uint32Array(6);
    let randomBufferFloat = new Float32Array(6);
    window.crypto.getRandomValues(randomBuffer);

    console.log('randomBuffer with random values:', randomBuffer); //

    for (let i = 0; i < randomBuffer.length; i++){
        let temp = randomBuffer[i] / (0xFFFFFFFF);
        console.log('Temp:', i, temp); //
        randomBufferFloat[i] = temp;
    }

    let count = 0;
    //
    console.log('randomBufferFloat after For:', randomBufferFloat) //

    // while set does not contain 6 values, create a random value between 1 and 60
    while (draw.size < 6) {
        // COMMENT
        let csRandomNumber = randomBufferFloat[count];
        console.log('csRandomNumber', count, csRandomNumber) //
        count += 1;
        min = Math.ceil(1);
        max = Math.floor(60);
        value = Math.floor(csRandomNumber * (max - min + 1) + min);
        // COMMENT Remove this and find a better way jesus
        while (draw.has(value)){
            if (value == 60){
                value = 30;
            }
            value = value +1;
        }
        // sets cannot contain duplicates so value is only added if it does not exist in set
        draw.add(value)
        console.log('Draw:', count, draw); //
    }

    // turn set into an array
    let a = Array.from(draw);

    // sort array into size order
    a.sort(function (a, b) {
        return a - b;
    });

    // add values to fields in create draw form
    for (let i = 0; i < 6; i++) {
        document.getElementById("no" + (i + 1)).value = a[i];
    }
}