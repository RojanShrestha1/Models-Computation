from ruleshield.ambiguity import ambiguous_rule_trees, corrected_rule_structure, demonstrate


def test_ambiguous_grammar_two_trees():
    trees = ambiguous_rule_trees(["RULE1", "RULE2", "RULE3"])
    assert trees["left_grouped"] != trees["right_grouped"]
    assert trees["left_grouped"] == "((RULE1 RULE2) RULE3)"
    assert trees["right_grouped"] == "(RULE1 (RULE2 RULE3))"


def test_corrected_grammar_predictable_and_no_universal_claim():
    assert corrected_rule_structure(["RULE1", "RULE2"]).endswith("epsilon")
    result = demonstrate()
    assert result.accepted
    assert "No universal ambiguity detector" in result.metadata["universal_detection_claim"]
