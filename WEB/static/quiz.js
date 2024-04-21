document.addEventListener('DOMContentLoaded', function() {
    let currentQuiz = null;
    let currentQuestionIndex = 0;
    let score = 0;

    const quizzes = [
        {
            title: "Značky aut a jejich původ",
            description: "Testujte své znalosti o původu známých automobilových značek.",
            questions: [
                {
                    question: "Která země je domovem automobilky 'Volkswagen'?",
                    options: ["USA", "Německo", "Švédsko", "Jižní Korea"],
                    answer: 1
                },
                {
                    question: "Kde byla založena automobilka 'Ford'?",
                    options: ["USA", "Velká Británie", "Německo", "Austrálie"],
                    answer: 0
                },
                {
                    question: "Která země je domovem automobilky 'Toyota'?",
                    options: ["Japonsko", "Čína", "Německo", "Austrálie"],
                    answer: 0
                },
                {
                    question: "Z které země pochází automobilka 'Hyundai'?",
                    options: ["Jižní Korea", "Japonsko", "Čína", "Indie"],
                    answer: 0
                },
                {
                    question: "Která země je domovem automobilky 'Fiat'?",
                    options: ["Itálie", "Francie", "Německo", "Španělsko"],
                    answer: 0
                },
                {
                    question: "Kde byla založena automobilka 'Peugeot'?",
                    options: ["Francie", "Itálie", "Belgie", "Švýcarsko"],
                    answer: 0
                },
                {
                    question: "Která země je domovem automobilky 'Honda'?",
                    options: ["Čína", "Japonsko", "Jižní Korea", "Indie"],
                    answer: 1
                },
                {
                    question: "Kde byla založena automobilka 'Chevrolet'?",
                    options: ["Kanada", "USA", "Mexiko", "Brazílie"],
                    answer: 1
                },
                {
                    question: "Která země je domovem automobilky 'Renault'?",
                    options: ["Španělsko", "Itálie", "Francie", "Německo"],
                    answer: 2
                },
                {
                    question: "Z které země pochází automobilka 'Saab'?",
                    options: ["Švédsko", "Norsko", "Dánsko", "Finsko"],
                    answer: 0
                },
                {
                    question: "Která země je domovem automobilky 'Seat'?",
                    options: ["Španělsko", "Itálie", "Portugalsko", "Francie"],
                    answer: 0
                },
                {
                    question: "Kde byla založena automobilka 'Skoda'?",
                    options: ["Česká republika", "Slovensko", "Polsko", "Maďarsko"],
                    answer: 0
                },
                {
                    question: "Která země je domovem automobilky 'Lexus'?",
                    options: ["Čína", "Jižní Korea", "Japonsko", "Tchaj-wan"],
                    answer: 2
                },
                {
                    question: "Kde byla založena automobilka 'Jaguar'?",
                    options: ["USA", "Velká Británie", "Německo", "Austrálie"],
                    answer: 1
                },
                {
                    question: "Která země je domovem automobilky 'Volvo'?",
                    options: ["Švédsko", "Norsko", "Dánsko", "Finsko"],
                    answer: 0
                },
                {
                    question: "Z které země pochází automobilka 'Opel'?",
                    options: ["Španělsko", "Itálie", "Německo", "Francie"],
                    answer: 2
                },
                {
                    question: "Kde byla založena automobilka 'Kia'?",
                    options: ["Jižní Korea", "Japonsko", "Čína", "Indie"],
                    answer: 0
                },
                {
                    question: "Která země je domovem automobilky 'Mazda'?",
                    options: ["Čína", "Japonsko", "Jižní Korea", "Tchaj-wan"],
                    answer: 1
                },
                {
                    question: "Z které země pochází automobilka 'Citroën'?",
                    options: ["Německo", "Itálie", "Francie", "Španělsko"],
                    answer: 2
                },
                {
                    question: "Kde byla založena automobilka 'Bentley'?",
                    options: ["Velká Británie", "USA", "Německo", "Švýcarsko"],
                    answer: 0
                },
                {
                    question: "Která země je domovem automobilky 'Aston Martin'?",
                    options: ["USA", "Velká Británie", "Německo", "Itálie"],
                    answer: 1
                },
                {
                    question: "Z které země pochází automobilka 'Alfa Romeo'?",
                    options: ["Itálie", "Francie", "Německo", "Španělsko"],
                    answer: 0
                },
                {
                    question: "Kde byla založena automobilka 'Porsche'?",
                    options: ["Německo", "Švýcarsko", "Rakousko", "Itálie"],
                    answer: 0
                },
                {
                    question: "Která země je domovem automobilky 'Bugatti'?",
                    options: ["Francie", "Německo", "Itálie", "Švýcarsko"],
                    answer: 0
                },
                {
                    question: "Z které země pochází automobilka 'Lamborghini'?",
                    options: ["Itálie", "Německo", "Francie", "Španělsko"],
                    answer: 0
                },
            ]
        },
        {
            title: "Historie motorismu",
            description: "Otestujte své znalosti historie motorových sportů.",
            questions: [
                {
                    question: "Který rok se konal první závod Grand Prix ve Formuli 1?",
                    options: ["1950", "1945", "1955", "1960"],
                    answer: 0
                },
                {
                    question: "Kdo je známý jako první vítěz závodu 24 hodin Le Mans?",
                    options: ["Ferdinand Porsche", "André Lagache", "Henry Ford", "Enzo Ferrari"],
                    answer: 1
                },
                {
                    question: "Který jezdec vyhrál Formuli 1 nejvícekrát v 90. letech?",
                    options: ["Michael Schumacher", "Ayrton Senna", "Alain Prost", "Nigel Mansell"],
                    answer: 0
                },
                {
                    question: "Jaký závod se tradičně považuje za nejnebezpečnější motoristický závod na světě?",
                    options: ["Isle of Man TT", "Dakar Rally", "Indy 500", "Nürburgring"],
                    answer: 0
                },
                {
                    question: "Která automobilka vyhrála první závod FIA World Endurance Championship?",
                    options: ["Audi", "Porsche", "Toyota", "Ferrari"],
                    answer: 1
                },
                {
                    question: "Kdo byl prvním pilotem, který vyhrál závod Formule 1 pro tým Ferrari?",
                    options: ["Juan Manuel Fangio", "Alberto Ascari", "Mike Hawthorn", "Niki Lauda"],
                    answer: 1
                },
                {
                    question: "V kterém roce byl založen slavný závodní tým McLaren?",
                    options: ["1963", "1966", "1970", "1975"],
                    answer: 1
                },
                {
                    question: "Jaký závod je známý tím, že se jede v ulicích města?",
                    options: ["Monaco Grand Prix", "Le Mans", "Silverstone", "Daytona"],
                    answer: 0
                },
                {
                    question: "Který rok byl oficiálně zahájen závod Dakar Rally?",
                    options: ["1978", "1982", "1985", "1990"],
                    answer: 0
                },
                {
                    question: "Kdo vyhrál Indianapolis 500 nejvícekrát?",
                    options: ["A.J. Foyt", "Rick Mears", "Al Unser", "Helio Castroneves"],
                    answer: 3
                },
                {
                    question: "Který jezdec získal titul ve Formuli 1 jak v 70. tak i 80. letech?",
                    options: ["Niki Lauda", "James Hunt", "Nelson Piquet", "Alan Jones"],
                    answer: 0
                },
                {
                    question: "Který závod byl poprvé zahrnut do Triple Crown of Motorsport?",
                    options: ["Le Mans", "Indy 500", "Monaco Grand Prix", "Sebring"],
                    answer: 1
                },
                {
                    question: "Který tým získal první pohár konstruktérů ve Formuli 1?",
                    options: ["Ferrari", "Williams", "McLaren", "Vanwall"],
                    answer: 3
                },
                {
                    question: "Jaký jezdec získal svůj první titul mistra světa ve Formuli 1 s týmem Red Bull?",
                    options: ["Sebastian Vettel", "Daniel Ricciardo", "Max Verstappen", "Mark Webber"],
                    answer: 0
                },
                {
                    question: "Které závodní okruhy se nazývá 'Zelené peklo'?",
                    options: ["Nürburgring", "Spa-Francorchamps", "Monza", "Silverstone"],
                    answer: 0
                },
                {
                    question: "Který jezdec získal první titul mistra světa ve Formuli E?",
                    options: ["Jean-Eric Vergne", "Nelson Piquet Jr.", "Sebastien Buemi", "Lucas di Grassi"],
                    answer: 1
                },
                {
                    question: "Kdo byl první žena, která získala body ve Formuli 1?",
                    options: ["Maria Teresa de Filippis", "Lella Lombardi", "Divina Galica", "Desiré Wilson"],
                    answer: 1
                },
                {
                    question: "Jaký motoristický závod se koná každoročně na ostrově Man?",
                    options: ["Manx Grand Prix", "Isle of Man TT", "Man Rally", "Isle of Man Race"],
                    answer: 1
                },
                {
                    question: "Kdo je známý jako 'Král Rally'?",
                    options: ["Sebastien Loeb", "Colin McRae", "Carlos Sainz", "Walter Röhrl"],
                    answer: 0
                },
                {
                    question: "Který jezdec vyhrál titul ve Formuli 1 ve své debutové sezóně?",
                    options: ["Lewis Hamilton", "Jacques Villeneuve", "Juan Manuel Fangio", "Nico Rosberg"],
                    answer: 1
                },
                {
                    question: "Kterému závodníkovi se přezdívá 'Profesor'?",
                    options: ["Alain Prost", "Ayrton Senna", "Michael Schumacher", "Niki Lauda"],
                    answer: 0
                },
                {
                    question: "Který rok získal Michael Schumacher svůj první titul ve Formuli 1?",
                    options: ["1994", "1995", "1996", "1997"],
                    answer: 0
                },
                {
                    question: "Která automobilka dosáhla prvního vítězství ve Formuli 1 s hybridním motorem?",
                    options: ["Mercedes", "Ferrari", "Red Bull", "McLaren"],
                    answer: 0
                },
                {
                    question: "Který závodník vyhrál nejvíce závodů ve Formuli 1 bez zisku mistrovského titulu?",
                    options: ["Stirling Moss", "David Coulthard", "Rubens Barrichello", "Felipe Massa"],
                    answer: 0
                },
                {
                    question: "Který závodní okruh hostil první noční závod ve Formuli 1?",
                    options: ["Marina Bay Street Circuit", "Bahrain International Circuit", "Yas Marina Circuit", "Suzuka Circuit"],
                    answer: 0
                }
            ]
        }
    ];
    function generateQuizCards() {
        const container = document.getElementById('quiz-list');
        quizzes.forEach((quiz, index) => {
            const cardHTML = `
                <div class="col-md-4">
                    <div class="card card-custom">
                        <div class="card-body">
                            <h5 class="card-title">${quiz.title}</h5>
                            <p class="card-text">${quiz.description}</p>
                            <button class="btn btn-primary start-quiz-btn" data-quiz-index="${index}">Spustit kvíz</button>
                        </div>
                    </div>
                </div>
            `;
            container.innerHTML += cardHTML;
        });

        document.querySelectorAll('.start-quiz-btn').forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-quiz-index'));
                startQuiz(index);
            });
        });
    }

    function startQuiz(index) {
        currentQuiz = quizzes[index];
        currentQuestionIndex = 0;
        score = 0;
        showQuestion(currentQuestionIndex);
        $('#quizModal').modal('show');
    }

    function showQuestion(questionIndex) {
        const question = currentQuiz.questions[questionIndex];
        const quizContainer = document.getElementById('quiz-container');
        const optionsHtml = question.options.map((option, index) => 
            `<div class="form-check">
                <input class="form-check-input" type="radio" name="option" id="option${index}" value="${index}">
                <label class="form-check-label" for="option${index}">
                    ${option}
                </label>
            </div>`
        ).join('');

        quizContainer.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${question.question}</h5>
                    <form>${optionsHtml}</form>
                </div>
            </div>
        `;

        document.getElementById('next-btn').style.display = (questionIndex < currentQuiz.questions.length - 1) ? 'inline-block' : 'none';
        document.getElementById('finish-btn').style.display = 'inline-block';
        document.getElementById('finish-btn').onclick = endQuiz;  // Ujistěte se, že funkce endQuiz je správně přiřazená.
    }

    function endQuiz() {
        // Zkontrolujte, jestli byla vybrána odpověď v poslední otázce
        const selectedOption = document.querySelector('input[name="option"]:checked');
        if (selectedOption && parseInt(selectedOption.value) === currentQuiz.questions[currentQuestionIndex].answer) {
            score++;
        }

        const quizContainer = document.getElementById('quiz-container');
        quizContainer.innerHTML = `<h4>Váš výsledek: ${score} z ${currentQuiz.questions.length}</h4>`;
        document.getElementById('next-btn').style.display = 'none';
        document.getElementById('finish-btn').style.display = 'none';
        setTimeout(() => {
            $('#quizModal').modal('hide');
        }, 2000);
    }

    generateQuizCards();  // Generuje karty kvízů při načtení stránky
});