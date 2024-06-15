import CollectionCard from '../../components/CollectionCard/CollectionCard'
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
} 