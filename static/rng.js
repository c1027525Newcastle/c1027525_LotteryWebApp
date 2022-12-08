// JavaScript function to generate 6 random unique values in order and populate form
function luckyDip() {

    // create empty set
    let draw = new Set();

    // COMMENT
    let randomBuffer = new Uint32Array(6);
    let randomBufferFloat = new Float32Array(6);
    window.crypto.getRandomValues(randomBuffer);

    for (let i = 0; i < randomBuffer.length; i++){
        randomBufferFloat[i] = randomBuffer[i] / (0xFFFFFFFF);
    }
    //

    let min;
    let max;
    let value;
    let count = 0;
    // while set does not contain 6 values, create a random value between 1 and 60
    while (draw.size < 6) {
        // COMMENT
        let csRandomNumber = randomBufferFloat[count];
        min = Math.ceil(1);
        max = Math.floor(60);
        value = Math.floor(csRandomNumber * (max - min + 1) + min);
        // Check is value is already in draw and make a new cryptographic secure one
        while (draw.has(value)) {
            let newRandomBuffer = new Uint32Array(1);
            window.crypto.getRandomValues(newRandomBuffer);
            let newcsRandomNumber = newRandomBuffer[0] / (0xFFFFFFFF);
            value = Math.floor(newcsRandomNumber * (max - min + 1) + min);
        }
        count += 1;
        // sets cannot contain duplicates so value is only added if it does not exist in set
        draw.add(value);
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