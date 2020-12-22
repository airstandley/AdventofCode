import java.io.File

fun getInput(filename: String): List<String> {
    return File(filename).readLines()
}

fun parseInput(input: List<String>): Pair<Int, List<Int?>> {
    assert(input.size == 2)
    val timestamp: Int = input[0].toInt()
    val busIds = mutableListOf<Int?>()
    val ids: List<String> = input[1].split(',')
    for (id in ids) {
        if(id == "x") {
            busIds.add(null)
        } else {
            busIds.add(id.toInt())
        }
    }
    return Pair(timestamp, busIds)
}

fun getNextBus(initialTimestamp: Int, ids: List<Int>): Pair<Int, Int> {
    // Return the Bus and Timestamp for the next available bus.
    var timestamp = initialTimestamp
    // If a bus doesn't depart by twice the initial then it probably never will.
    while (timestamp < initialTimestamp * 2) {
        val departingBuses = ids.filter { id -> (timestamp.rem(id) == 0) }
        if (!departingBuses.isEmpty()) {
            // Return the first match since the problem is set up in such
            // a wat that it's assume no id is a multiple of another id.
            return Pair(timestamp, departingBuses.first())
        }
        timestamp++
    }
    throw Exception("No departing bus found!")
}

const val ZERO: Long = 0
fun getSequentialTimestampBRUTE(ids: List<Int?>): Long {
    // Brute Force!!!
    var initialTimestamp: Long = 0
    while (true) {
        var timestamp = initialTimestamp
        var match = true
        for (id in ids) {
            if (id != null) {
                if (timestamp.rem(id) != ZERO) {
                    // Bus does not depart
                    match = false
                    break
                }
            }
            timestamp++
        }
        if (match) {
            return initialTimestamp
        }
        initialTimestamp++
    }
}

fun getSequentialTimestampBRUTE2(ids: List<Int?>): Long {
    val idGaps = mutableListOf<Pair<Int,Int>>()
    var gap = 1
    for (id in ids) {
        if(id == null) {
            gap++
        } else {
            idGaps.add(Pair(id, gap))
            gap = 1
        }
    }

    val multiples = mutableListOf<Int>()
    idGaps.forEach { id -> multiples.add(1) }
    var i = 1
    while (i < idGaps.size) {
        if (i == 0){
            i++
            continue
        }
        val gap = idGaps[i].second
        val a = idGaps[i-1].first
        val b = idGaps[i].first
        if(a*multiples[i-1]+gap == b*multiples[i]) {
            //matched
            i++
        } else if (a*multiples[i-1]+gap < b * multiples[i]) {
            // Check next departure of A
            multiples[i-1]++
            i--
        } else {
            // Check next departure of B
            multiples[i]++
        }
    }
    return idGaps[0].first.toLong()*multiples[0].toLong()
}

const val ONE: Long = 1
fun modInverse(number:Long, mod: Long): Long {
    // xi[1] => 35xi ≡ 1 (mod 2) => xi ≡ 1 (mod 2) -> 1 (1%2=1)
    // xi[2] => 14xi ≡ 1 (mod 5) => 4xi ≡ 1 (mod 5) -> not 1, not 2, not 3, 4 (16%5=1)
    // xi[3] => 10xi ≡ 1 (mod 7) => 3xi ≡ 1 (mod 7) -> not 1, not 2, not 3, not 4, 5 (15%7=1)

    val target = number.rem(mod)
    for (i in 1..mod) {
        if ((target*i).rem(mod) == ONE) {
            return i
        }
    }
    throw Exception("No Inverse. Number: $number Mod: $mod")
}

fun chineseRemainder(congruences: List<Pair<Int, Int>>): Long {
    // Simultaneous congruences
    // t ≡ 0 (mod 2)
    // t ≡ 4 (mod 5)
    // t ≡ 5 (mod 7)

    // CRT (N=70)
    var bigN:Long = 1
    congruences.forEach { congruence -> bigN *= congruence.second }
    // bi  Ni  xi  bNx
    // 0   35  1   0
    // 4   14  4   224
    // 5   10  5   250
    var sum: Long = 0
    for (congruence in congruences) {
        val bi = congruence.first
        val bigNi = bigN/congruence.second
        val xi = modInverse(bigNi, congruence.second.toLong())
        sum += (bi*bigNi*xi)
    }
    // 474
    // t = 474 (mod 70) => t = 54 (55,56)
    return sum.rem(bigN)
}

fun getSequentialTimestamp(ids: List<Int?>): Long {
    // Cheat and check reddit to find out about a random theorem that I've never heard of that is apparently really
    // well know in modulo mathematics. (Because apparently that was supposed to be obvious).
    // Chinese Remainder Theorem time.

    // 2, 5 , 7
    // Answer to 2, 5 is 2*t modulo 5 = -1 (2*3 = 9 mod 5 = -1) => (t ≡ -1 (mod 5) ) => (t ≡ 4 (mod 5) )
    // Answer to 5, 7 is 5*t modulo 7 = -1 (5*4 = 20 mod 7 = -1) => (t+1 ≡ -1 (mod 7)) -> (t ≡ -2 (mod 7)) => (t ≡ 5 mod(7))

    // 7,13,x,x,59,x,31,19
    // t ≡ 0 (mod 7)
    // t+1 ≡ 0 (mod 13) => t ≡ -1 (mod 13) => t ≡ 12 (mod 13)
    // t+4 ≡ 0 (mod 59) => t ≡ -4 (mod 59) => t ≡ 55 (mod 59)
    val congruences = mutableListOf<Pair<Int, Int>>()
    for (i in ids.indices) {
        if (ids[i] != null) {
            val mod = ids[i] as Int
            var rem = 0 - i
            if (rem < 0) {
                rem += mod
            }
            congruences.add(Pair(rem, mod))
        }
    }
    return chineseRemainder(congruences)
}


fun main(args: Array<String>) {
    val input = parseInput(getInput("Input"))
    val timestamp = input.first
    val ids = input.second
    val output = getNextBus(timestamp, ids.filter { id -> id != null } as List<Int>)
    val departing = output.first
    val bus = output.second
    val solutionOne = (departing - timestamp) * bus
    println("First Solution: $solutionOne")
    val solutionTwo = getSequentialTimestamp(ids)
    println("Second Solution: $solutionTwo")
}