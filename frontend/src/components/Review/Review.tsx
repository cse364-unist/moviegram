import myImage from '../../../public/images/toy-story.jpg';

export default function Review() {
    // Dummy data for reviews
    const reviews = [
        { id: 1, content: "Bad cartoon!" },
        { id: 2, content: "I like this cartoon!!! wooooooooow very good!" },
        { id: 3, content: "I like this cartoon!!!" },
        { id: 4, content: "I like this cartoon!!!" },
    ];

    return (
        <div className="w-100 shadow-md shadow-black rounded-md mt-5">
            <p className='pt-2 pb-0 text-sm font-sans pl-2'>Aibek left a review </p>
            <div className='mt-0 mb-0 divider'></div>
            <img src={myImage} alt='Review image' />
            <div className='mt-4 mb-0 divider'></div>

            <div className='flex'>
                <div className="rating ml-2">
                    <input type="radio" name="rating-4" className="mask mask-star-2 bg-green-500" />
                    <input type="radio" name="rating-4" className="mask mask-star-2 bg-green-500" checked />
                    <input type="radio" name="rating-4" className="mask mask-star-2 bg-green-500" />
                    <input type="radio" name="rating-4" className="mask mask-star-2 bg-green-500" />
                    <input type="radio" name="rating-4" className="mask mask-star-2 bg-green-500" />
                </div>
                <p className='text-sm font-sans pl-1'>100 rated</p>
            </div>

            <div className='ml-2 mr-2 mt-2'>
                <input type="text" placeholder="Add review..." className="input input-bordered input-success w-full max-w-xs" />
                <div>
                    {reviews.map(review => (
                        <p key={review.id} className="text-sm bg-gray-100 rounded-md p-1.5 mt-2 mb-2">{review.content}</p>
                    ))}
                    {reviews.length > 3 && <button className="text-sm text-blue-500">Show more</button>}
                </div>
            </div>
        </div>
    );
}
