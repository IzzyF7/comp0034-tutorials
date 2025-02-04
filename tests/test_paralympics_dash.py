import requests
from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains


def test_server_live(dash_duo):
    """
    GIVEN the app is running
    WHEN an HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Start the app in a server
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    # Get the url for the web app root
    # You can print this to see what it is e.g. print(f'The server url is {url}')
    url = dash_duo.driver.current_url

    # Requests is a python library and here is used to make an HTTP request to the sever url
    response = requests.get(url)

    # Finally, use the pytest assertion to check that the status code in the HTTP response is 200
    assert response.status_code == 200


def test_home_h1_text_equals(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the H1 heading with an id of 'title' should have the text "Paralympics Data Analytics"
    """
    # As before, use the import_app to run the Dash app in a threaded server
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Wait for the H1 heading to be available on the page, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("h1", timeout=4)  # Dash function version

    # Find the text content of the H1 heading element
    h1_text = dash_duo.find_element("h1").text  # Dash function version

    # Assertion checks that the heading has the expected text
    assert h1_text == "Paralympics Data Analytics"

# Find the dropdown selector and check it has one of the expected values (events, sports, countries).
def test_dropdown_selector(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the dropdown selector with an id of 'dropdown-input' should have the options "Events", "Sports", "Countries", and "Participants"
    """
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)
    
    dash_duo.wait_for_element("#dropdown-input", timeout=4)  # Dash function version

    # Find the dropdown element
    dropdown = dash_duo.find_element("#dropdown-input")  # Use '#' for ID in Dash tests

    # Get the options in the dropdown
    from selenium.webdriver.common.by import By

    options = dropdown.find_elements(By.TAG_NAME, "option")

    # Check that at least one of the options is "Events"
    assert any(option.text == "Events" for option in options)

import time

def test_checkbox_graph(dash_duo):
    """
    GIVEN the app is loaded
    AND a checkbox is present on the page
    AND a bar chart is displayed on the page
    WHEN the checkbox selection is changed
    THEN the chart should be updated
    """

    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    dash_duo.wait_for_element("#checklist-input", timeout=4)  # Dash function version

    # Find the bar chart element
    bar_chart = dash_duo.find_element("#bar-div")

    # count the number of elements in the bar chart with the class 'dash-graph'
    initial_count = len(bar_chart.find_elements(By.CLASS_NAME, "dash-graph"))

    # Select the 'Winter' checkbox element. Summer is already selected.

    # Click the checkbox with the value of 'winter'
    dash_duo.find_element("#checklist-input input[value='winter']").click()

    # Wait 2 seconds for the chart to update
    time.sleep(2)

    # count the number of elements in the bar chart with the class 'dash-graph'
    updated_count = len(bar_chart.find_elements(By.CLASS_NAME, "dash-graph"))

    # Check that the updated count is greater than the initial count
    assert updated_count > initial_count

def test_line_chart_selection(dash_duo):
    """
    GIVEN the app is running
    WHEN the dropdown for the line chart is changed to
    THEN the heading text should change to reflect the selection
    """
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # To find an element by id you use '#id-name'; to find an element by class use '.class-name'
    dash_duo.wait_for_element("#dropdown-input", timeout=2)

    # See https://github.com/plotly/dash/blob/dev/components/dash-core-components/tests/integration/dropdown/test_dynamic_options.py#L31
    # Not easy to follow but give syntax for selecting values in a dropdown list
    dropdown_input = dash_duo.find_element("#dropdown-input")
    dropdown_input.send_keys("Sports")
    dash_duo.driver.implicitly_wait(2)

    # Run the app and use Chrome browser, find the element, right click and choose Select, find the element in the 
    # Elements console and select 'copy selector'. Pate this as the value of the variable e.g. see css_selector below.
    css_selector = '#line-chart > div.js-plotly-plot > div > div > svg:nth-child(3) > g.infolayer > g.g-gtitle > text'
    chart_title = dash_duo.find_element(css_selector)
    assert ("sports" in chart_title.text), "'sports' should appear in the chart title"

def test_map_hover(dash_duo):
    """
    GIVEN the app is running which has a <div id='map>
    THEN there should not be any elements with a class of 'card' one the page
    WHEN a marker in the map is selected
    THEN there should be one more card on the page then there was at the start
    AND there should be a text value for the h6 heading in the card
    """
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Wait for the map to be available on the page
    dash_duo.wait_for_element("#map", timeout=4)

    # There is no card so finding elements with a bootstrap class of 'card' should return 0
    cards = dash_duo.driver.find_elements(By.CLASS_NAME, "card")
    cards_count_start = len(cards)

    # Find the first map marker
    marker_selector = '#map > div.js-plotly-plot > div > div > svg:nth-child(1) > g.geolayer > g > g.layer.frontplot > g > g > path:nth-child(1)'
    marker = dash_duo.driver.find_element(By.CSS_SELECTOR, marker_selector)

    # Use the Actions API and build a chain to move to the marker and hover
    ActionChains(dash_duo.driver).move_to_element(marker).pause(1).perform()

    # Check there is now 1 card on the page
    dash_duo.wait_for_element(".card", timeout=5)
    cards_end = dash_duo.driver.find_elements(By.CLASS_NAME, "card")
    cards_count_end = len(cards_end)
    # There should be 1 more card
    assert cards_count_end - cards_count_start == 1




