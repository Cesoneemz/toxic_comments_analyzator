package main

import (
	"bytes"
	"encoding/json"
	"html/template"
	"log"
	"net/http"
)

type Comment struct {
	Text string `json:"text"`
}

type PredictionResponse struct {
	Text  string `json:"text"`
	Label string `json:"label"`
}

func main() {
	http.HandleFunc("/", homeHandler)
	http.HandleFunc("/predict", predictHandler)

	log.Println("Server started at :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func homeHandler(w http.ResponseWriter, r *http.Request) {
	tmpl := template.Must(template.ParseFiles("index.html"))
	if err := tmpl.Execute(w, nil); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

func predictHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Invalid request method", http.StatusMethodNotAllowed)
		return
	}

	text := r.FormValue("text")
	comment := Comment{Text: text}

	jsonComment, err := json.Marshal(comment)
	if err != nil {
		http.Error(w, "Failed to marshal JSON", http.StatusInternalServerError)
		return
	}

	resp, err := http.Post("http://api:8000/predict/", "application/json", bytes.NewBuffer(jsonComment))
	if err != nil {
		http.Error(w, "Failed to make request to API", http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	var predictionResponse PredictionResponse
	if err := json.NewDecoder(resp.Body).Decode(&predictionResponse); err != nil {
		http.Error(w, "Failed to decode API response", http.StatusInternalServerError)
		return
	}

	if predictionResponse.Label == "Toxic" {
		predictionResponse.Label = "Токсичный"
	} else {
		predictionResponse.Label = "Не токсичный"
	}

	tmpl := template.Must(template.ParseFiles("index.html"))
	if err := tmpl.Execute(w, predictionResponse); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}
