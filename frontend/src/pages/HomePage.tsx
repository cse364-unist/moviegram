import "./HomePage.css"
import Review from "../components/Review/Review"

export default function HomePage() {
    return (
        <div className="feed">
            <div className="activities">
                <Review />
                <Review />
            </div>
        </div>
    )
} 