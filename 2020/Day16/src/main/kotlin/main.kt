import java.io.File
import java.lang.reflect.Field

fun getInput(filename: String): List<String> {
    return File(filename).readLines()
}

data class FieldRule(val name: String, val rangeOne: Pair<Int, Int>, val rangeTwo: Pair<Int, Int>)

fun parseRange(rangeString: String): Pair<Int, Int> {
    val parts = rangeString.split("-")
    val lower = parts[0].toInt()
    val upper = parts[1].toInt()
    return Pair(lower, upper)
}

fun parseFieldRule(ruleString: String): FieldRule {
    val parts = ruleString.split(": ")
    val name = parts[0]
    val ranges = parts[1].split(" or ")
    val rangeOne = parseRange(ranges[0])
    val rangeTwo = parseRange(ranges[1])
    return FieldRule(name, rangeOne, rangeTwo)
}

fun parseTicket(ticketString: String): List<Int> {
    val numbers = mutableListOf<Int>()
    for (number in ticketString.split(",")) {
        numbers.add(number.toInt())
    }
    return numbers
}

const val PARSING_NONE = "none"
const val PARSING_RULES = "rules"
const val PARSING_MY_TICKET = "mine"
const val PARSING_NEARBY_TICKETS = "nearby"

fun parseInput(input: List<String>): Triple<List<FieldRule>, List<Int>, List<List<Int>>> {
    var parsing = PARSING_RULES
    val rules = mutableListOf<FieldRule>()
    var myTicket: List<Int> = listOf()
    val nearbyTickets = mutableListOf<List<Int>>()
    for (line in input) {
        if (line.isEmpty()) {
            // End of Block
            parsing = PARSING_NONE
            continue
        } else if (line == "your ticket:") {
            parsing = PARSING_MY_TICKET
            continue
        } else if (line == "nearby tickets:") {
            parsing = PARSING_NEARBY_TICKETS
            continue
        }
        when(parsing) {
            PARSING_RULES -> {
                rules.add(parseFieldRule(line))
            }
            PARSING_MY_TICKET -> {
                myTicket = parseTicket(line)
            }
            PARSING_NEARBY_TICKETS -> {
                nearbyTickets.add(parseTicket(line))
            }
            PARSING_NONE -> throw Exception("Invalid Input: expected start of block, got $line")
        }
    }
    return Triple(rules, myTicket, nearbyTickets)
}

fun followsRule(value: Int, rule: FieldRule): Boolean {
    if ( rule.rangeOne.first <= value && value <= rule.rangeOne.second) {
        // In first range
        return true
    } else if (rule.rangeTwo.first <= value && value <= rule.rangeTwo.second) {
        // In second range
        return true
    }
    return false
}

fun getInvalidFieldsForTicket(ticket: List<Int>, rules: List<FieldRule>): List<Int> {
    val invalidFields = mutableListOf<Int>()
    for (field in ticket) {
        var valid = false
        for (rule in rules) {
            if (followsRule(field, rule)) {
                valid = true
                break
            }
        }
        if (!valid) {
            invalidFields.add(field)
        }
    }
    return invalidFields
}

fun getTicketScanningErrorRate(tickets: List<List<Int>>, rules: List<FieldRule>): Long {
    val ticketScanningErrors = mutableListOf<Int>()
    for (ticket in tickets) {
        ticketScanningErrors += getInvalidFieldsForTicket(ticket, rules)
    }
    var sum: Long = 0
    ticketScanningErrors.forEach { value -> sum += value }
    return sum
}

fun isTicketValid(ticket: List<Int>, rules: List<FieldRule>): Boolean {
    return getInvalidFieldsForTicket(ticket, rules).isEmpty()
}

fun getValidRules(value: Int, rules: List<FieldRule>): List<FieldRule> {
    val validRules = mutableListOf<FieldRule>()
    for (rule in rules) {
        if (followsRule(value, rule)){
            validRules.add(rule)
        }
    }
    return validRules
}

fun calculateFieldMap(myTicket: List<Int>, nearbyTickets: List<List<Int>>, rules: List<FieldRule>): Map<String, Int> {
    // Initialize the map of possible fields for each index
    val workingFieldMap = mutableMapOf<Int, List<FieldRule>>()
    // Use your ticket to create an initial list of possibilities
    for (i in myTicket.indices) {
        workingFieldMap[i] = getValidRules(myTicket[i], rules)
    }
    // Use the nearby tickets to narrow down the possible rules
    for (ticket in nearbyTickets) {
        for (i in ticket.indices) {
            workingFieldMap[i] = getValidRules(ticket[i], workingFieldMap.getOrDefault(i, rules))
        }
    }
    // Narrow down the remaining rules and construct the reverse map
    val fieldMap = mutableMapOf<String, Int>()
    var reduced = true
    while (reduced) {
        reduced = false
        for ((index, fields) in workingFieldMap) {
            val newFields = fields.filter { field -> (field.name !in fieldMap) }
            if (newFields.size == 1) {
                reduced = true
                val field = newFields.first().name
                fieldMap[field] = index
            }
            var inRules = ""
            fields.forEach { rule -> inRules += "${rule.name} " }
            var outRules = ""
            newFields.forEach { rule -> outRules += "${rule.name} " }
            workingFieldMap[index] = newFields
        }
    }
    return fieldMap
}

fun main(args: Array<String>) {
    val input = parseInput(getInput("Input"))
    val rules = input.first
    val ticket = input.second
    val nearbyTickets = input.third
    val errorRate = getTicketScanningErrorRate(nearbyTickets, rules)
    println("First Solution: $errorRate")
    val validNearbyTickets = nearbyTickets.filter { nearbyTicket -> isTicketValid(nearbyTicket, rules) }
    val fieldMap = calculateFieldMap(ticket, validNearbyTickets, rules)
    val fieldList = mutableListOf<Pair<String, Int>>()
    fieldMap.forEach {(name, index) -> fieldList.add(Pair(name, index)) }
    fieldList.sortBy { pair -> pair.second }
    var fieldString = ""
    fieldList.forEach { pair -> fieldString += "${pair.second}: ${pair.first}, "}
    var ticketString = ""
    fieldList.forEach { pair -> ticketString += "${pair.first}: ${ticket[pair.second]}, " }
    var sum: Long = 1
    for ((field, index) in fieldMap){
        if (field.contains("departure")) {
            sum *= ticket[index]
        }
    }
    println("Second Solution: $sum")
}