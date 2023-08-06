@WIP
Feature: Monkeytale Command Line Interface

    As a developer
    I want to run Monkeytale
    So that I can get debug information.

    Scenario Outline: Monkeytale version
        Given Monkeytale is installed
        When Monkeytale is executed using <COMMAND> with <OPTION>
        Then Monkeytale will complete successfully
        And Monkeytale will echo back its current version

        Examples:
            | COMMAND    | OPTION    |
            | monkeytale | --version |
            | @          | --version |

    Scenario: Monkeytale log
        Given Monkeytale is installed
        When Monkeytale is executed using monkeytale with None
        Then Monkeytale will complete successfully
        And Monkeytale will have produced a log file
