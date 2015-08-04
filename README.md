# alpha-mafia
A Question Answering System that can generate coherent questions from Wikipedia articles and answer questions about an article. We used various NLP libraries off the shelf for this.

Dependenices:
---

- Java1.7
- Pathon2.6
- RHEL packages for running numpy and scipy (BLAS and such)


Scripts:
---

Our scripts are called ask and answer, and are used accordingly

    Usage:

    ./ask article.txt nquestions
        article.txt - the article to ask questions about
        nquestions  - the number of questions to ask

    ./answer article.txt questions.txt
        article.txt  - the article to answer questions with
        question.txt - the questions to answer

When you have finished with our system, please remmeber to kill the BART server by running (the server is started automatically by the answer script)

    ./kill_server

Video
---

You can watch our final project video [here](https://www.youtube.com/watch?v=XuSXabda8uM)


