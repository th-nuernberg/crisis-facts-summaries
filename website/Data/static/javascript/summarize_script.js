// Initial Assignement for Button analyse
function initAssignment(){
    let button = document.getElementById("calculate_button");
    button.addEventListener("click",make_a_summary)
}



async function make_a_summary(){
   //if there is already a summary, remove it 
   if(document.getElementById("new_summary") != null){
    document.getElementById("new_summary").remove();
   }
 
   let ngramms = document.getElementById("ngram").value;
   // Check if Parameters have been entered
   if(!ngramms){ngramms = 2}

   let timespan = document.getElementById("time").value;
   // Check if Parameters have been entered, else set default parameter
   if(!timespan){timespan = 0}

   let weight = document.getElementById("weight").value;
   if(!weight){weight = 0}

   let max_length = document.getElementById("max_length").value;
   if(!max_length){max_length = 600}
   
   let summary_question = document.getElementById("text_area").value;
   if(!summary_question){summary_question = ""}

   // Make a json with all parameters, to be send to the backend
   let variables_for_summary = {"ngrams": ngramms, "timespan": timespan, "weight":weight, "max_length": max_length, "question": summary_question};
   let response_json;


   // Disable Analyse Button while function is calculating and styling
   let analyse_button = document.getElementById("calculate_button")
   analyse_button.style.opacity = 0.5
   analyse_button.style.cursor = "not-allowed"
   analyse_button.disabled = true

   //Show loading Cricle
   let loader = document.getElementById("load")
   loader.style.animation = "spin 2s linear infinite"
   loader.style.visibility = "visible"


   await fetch("http://127.0.0.1:5000/summarize", 
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            // Strigify the payload into JSON:
            body:JSON.stringify(variables_for_summary)
        }).then( (response) =>{
            if(response.ok){
                //alert(response.json());
                return response.json();     //It returns a promise which resolves with the result of parsing the body text as JSON
            }else{
                alert("something is wrong: Sind die Parameter gesetzt? Wenn nein, kann das bei dem Aufruf von gesamt() zu Problemen führen" + response.toString());
            }
        }).then(jsonResponse=>{

            o = JSON.stringify(jsonResponse);
            alert(o);
            //response_json = o;
            // Test Solution since Docker doesnt work well with windows
            response_json = jsonResponse
        }).catch((err) => console.error(err));


    //Hide loading circle; Enable Analyse Button when function is finished
    loader.style.visibility = "hidden"
    loader.style.animation = ""
    analyse_button.style.cursor = ""
    analyse_button.style.opacity = 1
    analyse_button.disabled = false;


   // Show new summary
   let main_Container = document.getElementById("Summary")

   let new_summary = document.createElement("p");
   new_summary.setAttribute('id', "new_summary");
   
   new_summary.setAttribute('align', "left");

   new_summary.innerHTML = response_json["sentences"];


   main_Container.append(new_summary);
   
}