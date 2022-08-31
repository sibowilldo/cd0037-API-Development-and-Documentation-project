import React, {Component} from 'react';
import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';

class QuestionView extends Component {
    constructor() {
        super();
        this.state = {
            questions: [],
            page: 1,
            totalQuestions: 0,
            categories: [],
            currentCategory: null,
            isDataLoaded: false
        };
    }

    componentDidMount() {
        this.getQuestions();
    }

    getQuestions = () => {
        fetch(`/questions?page=${this.state.page}`)
            .then(res => res.json())
            .then(result => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    categories: result.categories,
                    currentCategory: result.current_category.id,
                    isDataLoaded: true,
                });
            })
            .catch(error => {
                alert('Unable to load questions. Please try your request again')
            })
            .finally(() => {
                return
            })
    };

    selectPage(num) {
        this.setState({page: num}, () => this.getQuestions());
    }

    createPagination() {
        let pageNumbers = [];
        let maxPage = Math.ceil(this.state.totalQuestions / 10);
        for (let i = 1; i <= maxPage; i++) {
            pageNumbers.push(
                <span
                    key={i}
                    className={`page-num ${i === this.state.page ? 'active' : ''}`}
                    onClick={() => {
                        this.selectPage(i);
                    }}
                >
          {i}
        </span>
            );
        }
        return pageNumbers;
    }

    getByCategory = (id) => {
        fetch(`/categories/${id}/questions`)
            .then(res => res.json())
            .then(result => {
                this.setState({
                    questions: result.questions,
                    totalQuestions: result.total_questions,
                    currentCategory: result.current_category,
                });
            })
            .catch(error => {
                alert('Unable to load questions. Please try your request again');
            })
            .finally(() => {
                return
            })
    };

    submitSearch = (searchTerm) => {
        fetch('/questions', {
            method: 'POST',
            headers: {  'Content-Type': 'application/json' },
            credentials:'include',
            body: JSON.stringify({searchTerm: searchTerm})
        })
            .then(res => res.json())
            .then(result => {
                this.setState({
                questions: result.questions,
                totalQuestions: result.total_questions,
                currentCategory: result.current_category,
            });
            })
            .catch (error => {
                alert('Unable to load questions. Please try your request again')
            })
            .finally(()=>{
                return
            })
    };

    questionAction = (id) => (action) => {
        if (action === 'DELETE') {
            if (window.confirm('are you sure you want to delete the question?')) {
                fetch(`/questions/${id}`, {method: 'DELETE'})
                    .then(res => res.json())
                    .then(result => {
                        this.getQuestions()
                    }).catch(error => {
                        alert('Unable to load questions. Please try your request again');
                    }).finally(() => {
                        return;
                    })
            }
        }
    };

    render() {

        return (
            <div className='question-view'>
                <div className='categories-list'>
                    <h2
                        onClick={() => {
                            this.getQuestions();
                        }}
                    >
                        Categories
                    </h2>
                    <ul>
                        {this.state.categories.map((category) => (

                            <li key={category.id} onClick={() => {
                                this.getByCategory(category.id);
                            }}>
                                <div>{category.type}</div>
                                <img
                                    className='category'
                                    alt={`${category.type.toLowerCase()}`}
                                    src={`${category.type.toLowerCase()}.svg`}
                                />
                            </li>
                        ))}
                    </ul>
                    <Search submitSearch={this.submitSearch}/>
                </div>
                <div className='questions-list'>
                    <h2>Questions</h2>
                    {this.state.questions.map((q, ind) => (
                        <Question
                            key={q.id}
                            question={q.question}
                            answer={q.answer}
                            category={this.state.categories.find(cat => cat.id == q.category)}
                            difficulty={q.difficulty}
                            questionAction={this.questionAction(q.id)}
                        />
                    ))}
                    <div className='pagination-menu'>{this.createPagination()}</div>
                </div>
            </div>
        );
    }
}

export default QuestionView;
