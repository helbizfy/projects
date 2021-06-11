const startButton = document.getElementById("start-btn")
const nextButton = document.getElementById("next-btn")
const questionContainerElement = document.getElementById('question-container')

const questionElement = document.getElementById('question')
const answerButtonsElement = document.getElementById('answer-buttons')

let shuffledQuestions, currentQuestionIndex

startButton.addEventListener("click", startGame)
nextButton.addEventListener("click", () => {
    currentQuestionIndex++
    setNextQuestion()
})

function startGame() {
    console.log("Started")
    startButton.classList.add('hide')
    shuffledQuestions = questions.sort(() => Math.random() - .5)
    currentQuestionIndex = 0
    questionContainerElement.classList.remove('hide')
    setNextQuestion()

}

function setNextQuestion() {
    resetState()
    showQuestion(shuffledQuestions[currentQuestionIndex])

}

function showQuestion(question) {
    questionElement.innerText = question.question
    question.answers.forEach(answer => {
        const button = document.createElement('button')
        button.innerText = answer.text
        button.classList.add('btn')
        if (answer.correct) {
            button.dataset.correct = answer.correct
        }
        button.addEventListener('click', selectAnswer)
        answerButtonsElement.appendChild(button)
    })
}

function resetState() {
    clearStatusClass(document.body)
    nextButton.classList.add('hide')
    while (answerButtonsElement.firstChild) {
        answerButtonsElement.removeChild(answerButtonsElement.firstChild)
    }
}

function selectAnswer(e) {
    const selectedButton = e.target
    const correct = selectedButton.dataset.correct
    setStatusClass(document.body, correct)
    Array.from(answerButtonsElement.children).forEach(button => {
        setStatusClass(button, button.dataset.correct)
    })
    if (shuffledQuestions.length > currentQuestionIndex + 1) {
        nextButton.classList.remove('hide')
    } else {
        startButton.innerText = "Restart"
        startButton.classList.remove('hide')
    }


}

function setStatusClass(element, correct) {
    clearStatusClass(element)
    if (correct) {
        element.classList.add('correct')
    } else {
        element.classList.add('wrong')
    }
}

function clearStatusClass(element) {
    element.classList.remove('correct')
    element.classList.remove('wrong')
}

const questions = [
    {
        question: 'Kuram latviešu sportistam dota iesauka "Mūris"?',
        answers: [
            { text: 'Edgaram Masaļskim', correct: false },
            { text: 'Artūram Irbem', correct: true },
            { text: 'Kristeram Gudļevskim', correct: false },
            { text: 'Elvim Merzļikinam', correct: false },
        ]
    },
    {
        question: 'Nosauc šķēpmetēju, kurš 19.vasaras olimpiskajās spēlēs 1968.gadā Mehiko kļuva par olimpisko čempionu un kam piešķirts nosaukums „Visu laiku labākais Latvijas sportists”?',
        answers: [
            { text: 'Jānis Lūsis', correct: true },
            { text: 'Normunds Pildavs', correct: false },
            { text: 'Dainis Kūla', correct: false },
            { text: 'Mārcis Štrobinders', correct: false }
        ]
    },
    {
        question: 'Kura latviešu sportiste izcīnījusi pasaules čempiones titulu ātrslidošanā?',
        answers: [
            { text: 'Lāsma Kauniste', correct: true },
            { text: 'Sindija Klassena', correct: false },
            { text: 'Klaudija Pehšteine', correct: false },
            { text: 'Martina Sabļikova', correct: false }
        ]
    },
    {
        question: 'Kura ir pirmā Latvijā sarakstītā hronika?',
        answers: [
            { text: 'Livonijas hronika', correct: true },
            { text: 'Nameja hronika', correct: false },
            { text: 'Sēlijas hronika', correct: false },
            { text: 'Kokneses hronika', correct: false },
        ]
    },
    {
        question: 'Kura ir viena no vecākajām Latvijas aizsargājamajām dabas teritorijām, kas atrodas pie jūras?',
        answers: [
            { text: 'Slīteres Nacionālais parks', correct: true },
            { text: 'Ķemeru Nacionālais parks', correct: false },
            { text: 'Gaujas Nacionālais parks', correct: false },
            { text: 'Teiču rezervāts', correct: false }
        ]
    },
    {
        question: 'Pie kuras upes atrodas visvairāk alu?',
        answers: [
            { text: 'Pie Slocenes', correct: false },
            { text: 'Pie Gaujas', correct: true },
            { text: 'Pie Vēršupītes', correct: false },
            { text: 'Pie Abavas', correct: false }
        ]
    }
]