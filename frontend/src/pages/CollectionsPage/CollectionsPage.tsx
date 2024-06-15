/*import CollectionCard from '../../components/Collection/CollectionCard'
export default function CollectionsPage() {
    return (
        <div className="flex w-70 pt-16">
            <div className="w-20"> </div>
            <div className="w-60">
                <CollectionCard/>
            </div>
            <aside className="w-20"></aside>
        </div>
    )
}*/
import CollectionsList from '../../components/Collection/CollectionsList';
import PopularCollections from '../../components/Collection/PopularCollections';

import darkKnightPoster from '../../../public/images/dark_knight.jpg'; // Import the image
import inceptionPoster from '../../../public/images/inception.jpg';
import madmaxPoster from '../../../public/images/mad_max.jpg';
import diehardPoster from '../../../public/images/die_hard.jpg';

const collectionsData = [
  {
    title: 'Action Movies Collection',
    movies: [
      { title: 'The Dark Knight', poster: darkKnightPoster },
      { title: 'Inception', poster: inceptionPoster },
      { title: 'Mad Max: Fury Road', poster: madmaxPoster },
      { title: 'Die Hard', poster: diehardPoster }
    ]
  },
  {
    title: 'Comedy Movies Collection',
    movies: [
      { title: 'Superbad', poster: 'path/to/superbad.jpg' },
      { title: 'The Hangover', poster: 'path/to/hangover.jpg' },
      { title: 'Dumb and Dumber', poster: 'path/to/dumb_and_dumber.jpg' },
      { title: 'Anchorman: The Legend of Ron Burgundy', poster: 'path/to/anchorman.jpg' }
    ]
  },
  {
    title: 'Action Movies Collection',
    movies: [
      { title: 'The Dark Knight', poster: darkKnightPoster },
      { title: 'Inception', poster: inceptionPoster },
      { title: 'Mad Max: Fury Road', poster: madmaxPoster },
      { title: 'Die Hard', poster: diehardPoster }
    ]
  },
  {
    title: 'Action Movies Collection',
    movies: [
      { title: 'The Dark Knight', poster: darkKnightPoster },
      { title: 'Inception', poster: inceptionPoster },
      { title: 'Mad Max: Fury Road', poster: madmaxPoster },
      { title: 'Die Hard', poster: diehardPoster }
    ]
  }
];

export default function CollectionsPage() {
    return (
        <div>
        <main className="mt-20">
          <CollectionsList collections={collectionsData} />
          <div className="mt-8"></div>
          <PopularCollections collections={collectionsData} />
        </main>
    </div>
    )
}