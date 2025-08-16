function display(value) {
    const result = document.getElementById('result');
    result.value += value;
}

function calculate() {
    const result = document.getElementById('result');
    try {
        // Replace commas with dots for decimal calculation
        const expression = result.value.replace(/,/g, '.');
        
        // Evaluate the expression
        const calculationResult = eval(expression);
        
        // Check if result is finite
        if (!isFinite(calculationResult)) {
            result.value = 'Error';
        } else {
            result.value = calculationResult;
        }
    } catch (error) {
        // Display "Error" for invalid expressions
        result.value = 'Error';
    }
}

function clearScreen() {
    const result = document.getElementById('result');
    result.value = '';
}