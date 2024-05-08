import "./HomePage.css"
import Review from "../components/Review/Review"

export default function HomePage() {
    return (
        <div className="feed">
            <div className=""> </div>
            <div className="activities">
                <Review />
                <Review />
                <Review />
                <Review />
            </div>
        </div>
    )
} 