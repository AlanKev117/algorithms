// Linear-time = O(n) (tiempo)

function reorderFlights(flights) {
    // n = flights.length
    const sourceToDestinyMap = {} // O(1) origen -> destino
    const sourceToStepMap = {} // origen -> (origen, destino)
    const sourcesSet = new Set()
    const destiniesSet = new Set()

    for (let flight of flights) {
        // O(n)
        const [source, destiny] = flight
        sourceToDestinyMap[source] = destiny // asociar origen con destino pero ahora puedo buscar origen en tiempo O(1)
        sourceToStepMap[source] = flight
        sourcesSet.add(source)
        destiniesSet.add(destiny)
        // separo origenes de destinos
    }

    let firstSource;
    sourcesSet.forEach(source => {
        if (!destiniesSet.has(source)) {
            firstSource = source
        }
    }) // O(n)
    
    let source = firstSource
    const trip = []
    while (sourceToDestinyMap[source]) {
        // O(n)
        trip.push(sourceToStepMap[source])
        source = sourceToDestinyMap[source] //
    }
    // trip = [sfo, lax, jfk, bos, sea]
    // Total: 2 * O(n) + O(1) * 6 = O(n)
    return trip
}


console.log(
    reorderFlights([
        ["jfk", "bos"],
        ["sfo", "lax"],
        ["bos", "sea"],
        ["lax", "jfk"],
        // keys -> values
        // source -> dest
    ])
)
