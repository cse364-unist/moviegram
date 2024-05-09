// import "./HomePage.css"
import Review from "../../components/Review/Review"

export default function HomePage() {
    return (
        <div className="flex w-70 pt-16">
            <div className="w-20"> </div>
            <div className="w-60">
                <Review />
                <Review />
                <Review />
                <Review />
            </div>
            <aside className="w-20"></aside>
        </div>
    )
} 