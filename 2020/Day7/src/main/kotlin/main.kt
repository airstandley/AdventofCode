import java.io.File

fun getInput(): List<String> {
    return File("Input").readLines()
}

fun parseRule(line: String): Pair<String, MutableMap<String, Int>> {
    // Parse the rule to return a node
    var linkedNodes = mutableMapOf<String, Int>()
    // Drop the period and split on contains
    val parts = line.dropLast(1).split(" contain ")
    var bagNameParts = parts[0].split(" ")
    if (bagNameParts[bagNameParts.size - 1] != "bags") {
        throw Exception("Invalid Rule: Bag Name ${parts[0]} is not valid. Rule: $line")
    } else {
        bagNameParts = bagNameParts.dropLast(1)
    }
    val bagName = bagNameParts.joinToString(" ")
    if (parts[1] != "no other bags") {
        val containedBags = parts[1].split(", ")
        for (containedBag in containedBags) {
            var subParts = containedBag.split(" ")
            val number = subParts[0].toInt()
            if (number == 1) {
                if (subParts[subParts.size - 1] != "bag") {
                    throw Exception(
                        "Invalid Rule: Expected 'bag' not ${subParts[subParts.size - 1]} in $containedBag. Rule: $line"
                    )
                }
            } else {
                if (subParts[subParts.size - 1] != "bags") {
                    throw Exception(
                        "Invalid Rule: Expected 'bags' not '${subParts[subParts.size - 1]}' in '$containedBag'. Rule: $line"
                    )
                }
            }
            subParts = subParts.drop(1).dropLast(1)
            val containedBagName = subParts.joinToString(" ")
            linkedNodes[containedBagName] = number
        }
    }
    return Pair(bagName, linkedNodes)
}

fun parseRules(lines: List<String>): Pair<MutableMap<String, MutableMap<String, Int>>, MutableMap<String, MutableList<String>>> {
    // Parse the rules and return a forwards an backwards graph of contained bags
    val forwardsGraph = mutableMapOf<String, MutableMap<String , Int>>()
    val backwardGraph = mutableMapOf<String, MutableList<String>>()

    for (rule in lines) {
        val parsedRule = parseRule(rule)
        forwardsGraph[parsedRule.first] = parsedRule.second
        for (key in parsedRule.second.keys) {
            val list = backwardGraph.getOrElse(key) { mutableListOf() }
            list.add(parsedRule.first)
            backwardGraph[key] = list
        }
    }

    return Pair(forwardsGraph, backwardGraph)
}

fun findBagsThatCanContainBag(
    bagType: String, backwardGraph: MutableMap<String, MutableList<String>>, visitedNodes: Set<String>? = null
): MutableSet<String> {
    var containingBags =  mutableSetOf<String>()
    var childNodes = backwardGraph[bagType]?.toSet()
    val newVistedNodes: Set<String>
    if (childNodes != null) {
        containingBags = containingBags.union(childNodes) as MutableSet<String>
        // Vist the child nodes
        if (visitedNodes != null) {
            childNodes = childNodes.subtract(visitedNodes)
            newVistedNodes = visitedNodes.union(childNodes)
        } else {
            newVistedNodes = childNodes
        }
        for (node in childNodes) {
            if (visitedNodes != null) {
                if (visitedNodes.contains(node)) {
                    continue
                }
            }
            containingBags = containingBags.union(findBagsThatCanContainBag(node, backwardGraph, newVistedNodes)) as MutableSet<String>
        }
    }
    return containingBags
}

const val myBagType = "shiny gold"

fun main(args: Array<String>) {
    val graphs = parseRules(getInput())
    val containingBags = findBagsThatCanContainBag(myBagType, graphs.second)
    println("First Solution: ${containingBags.size}")
}