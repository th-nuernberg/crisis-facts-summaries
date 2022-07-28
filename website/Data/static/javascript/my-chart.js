var mychartObject = document.getElementById('myChart')

var chart = new Chart(mychartObject, {
    type: 'line',
    data: {
        labels: ["January", "February", "March", "April", "May", "June", "July", "August"],
        datasets: [{
            label: "Datensatz Nummer 1",
            backgroundColor: 'rgba(65,105,225,1)',
            borderColor: 'rgba(65,105,225,1)',
            data: [3,7,5,2,7,8,6,4]
        }]
    }
});