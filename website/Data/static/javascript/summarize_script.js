// Initial Assignement for Button analyse
function initAssignment(){
    let button = document.getElementById("calculate_button");
    button.addEventListener("click",make_a_summary)
}

//Create Options for Dataset
//TODO: TEST IN DOCKER
async function getDataset(){
    let response_json;
    await fetch("http://127.0.0.1:5000/datasets", 
        {
            method: 'GET',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
        }).then(jsonResponse=>{
            // Test Solution since Docker doesnt work well with windows
            response_json = jsonResponse
        }).catch((err) => console.error(err));

        let data_dropdown = document.getElementById("type_of_dataset");
        //alert(JSON.stringify(response_json))
        for(let i = 0; i < response_json["files"].length; i++){
            let new_option = document.createElement("option");
            new_option.setAttribute('class',"dropbtn_opt");
            new_option.setAttribute('value',response_json["files"][i]);
            new_option.innerHTML=response_json["files"][i];
            data_dropdown.appendChild(new_option);
       }    
}


async function make_a_summary(){
   //if there is already a summary, remove it 
   if(document.getElementById("new_summary") != null){
    document.getElementById("new_summary").remove();
   }
   //Get all Parameters
   let variables_for_summary = get_parameter_as_json();

   let response_json;

   // Disable Analyse Button while function is calculating and styling
   let analyse_button = document.getElementById("calculate_button");
   let loader = document.getElementById("load");

   close_button_show_loader(analyse_button,loader);

   //Send Data to Backend and await calculated results
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
                alert("something is wrong" + response.toString());
            }
        }).then(jsonResponse=>{

            o = JSON.stringify(jsonResponse);
            //alert(o);
            //response_json = o;
            // Test Solution since Docker doesnt work well with windows
            response_json = jsonResponse
        }).catch((err) => console.error(err));

    //Hide loading circle; Enable Analyse Button when function is finished
   open_button_hide_loader(analyse_button,loader);

   // Show new summary
   let main_Container = document.getElementById("Summary");

   let new_summary = document.createElement("p");
   new_summary.setAttribute('id', "new_summary");
   
   new_summary.setAttribute('align', "left");

   //Add each sentence of the summary with space between them
   for(let i = 0; i < response_json["sentences"].length; i++){
        new_summary.innerHTML += response_json["sentences"][i] + " ";
   }

   main_Container.append(new_summary);
}

function get_parameter_as_json(){
    
   let dataset = document.getElementById("type_of_dataset").value
   //Placehold, TODO A DATASET MUST BE CHOSEN
   if(!dataset){dataset = "empty"}

   let ngramms = document.getElementById("ngram").value;
   if(!ngramms){ngramms = 2}

   let max_length = document.getElementById("max_length").value;
   if(!max_length){max_length = 600}

   let date_from = document.getElementById("date_from").value;
   let time_from = document.getElementById("time_from").value;

   let date_to = document.getElementById("time_from").value;
   let time_to = document.getElementById("time_from").value;

   let function_type = document.getElementById("type_of_function").value;

   // Check if Parameters have been entered
   let summary_question = document.getElementById("text_area").value;
   if(!summary_question){summary_question = ""}
   
   // Make a json with all parameters, to be send to the backend
   let variables_for_summary = {"ngrams": ngramms,
                                "max_length": max_length,
                                "question": summary_question,
                                "timespan" : {"from": {"date":date_from, "time":time_from}, "to": {"date": date_to, "time":time_to}},
                                "function_type": function_type,
                                "dataset":dataset,    
                            };
   
   return variables_for_summary;
}

function close_button_show_loader(analyse_button,loader){
   analyse_button.style.opacity = 0.5
   analyse_button.style.cursor = "not-allowed"
   analyse_button.disabled = true

   //Show loading Cricle animation
   loader.style.animation = "spin 2s linear infinite"
   loader.style.visibility = "visible"
}

function open_button_hide_loader(analyse_button,loader){
   loader.style.visibility = "hidden"
   loader.style.animation = ""
   analyse_button.style.cursor = ""
   analyse_button.style.opacity = 1
   analyse_button.disabled = false;
}