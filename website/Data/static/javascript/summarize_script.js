//Mock Script for the Website
function initAssignment(){
    let button = document.getElementById("calculate_button");
    button.addEventListener("click",make_a_summary)
}



async function make_a_summary(){
   if(document.getElementById("new_summary") != null){
    document.getElementById("new_summary").remove();
   }
    
    //ALERT currently no check if data is valid
   let ngramms = document.getElementById("ngram").value;
   let timespan = document.getElementById("time").value;
   let weight = document.getElementById("weight").value;
   let max_length = document.getElementById("max_length").value;
   
   let summary_question = document.getElementById("text_area").value;

   let variables_for_summary = [{"ngrams": ngramms, "timespan": timespan, "weight":weight, "max_length": max_length, "question": summary_question}];


   await fetch("http://127.0.0.1:5000/summarize", 
        {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'Accept': 'application/json'
            },
            // Strigify the payload into JSON:
            body:JSON.stringify(variables_for_summary)}).then(res=>{
            if(res.ok){
                return res.json()
            }else{
                alert("something is wrong")
            }
        }).then(jsonResponse=>{
            let response = jsonResponse;
            response_json = response.json()
        } 
    ).catch((err) => console.error(err));



    // To Do  use response Object for summary

   let main_Container = document.getElementById("Summary")

   let new_summary = document.createElement("p");
   new_summary.setAttribute('id', "new_summary");
   
   new_summary.setAttribute('align', "left");

   new_summary.innerHTML =`A new Summary with ${ngramms} word-gramms, over the timespan of hour ${timespan}, with the weight of ${weight} and the maximum length of ${max_length} words.`;


   main_Container.append(new_summary);
   
}