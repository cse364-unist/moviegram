import './Review.css'
import myImage from '../../../public/images/toy-story.jpg'

export default function Review(){
    return (
        <div className="review_wrapper">
            <p>Aibek left a review </p> 
            <img className='review_img' src={myImage} alt='Review image'/>
            <p> I like this cartoon!!!</p>
        </div>
    )
}