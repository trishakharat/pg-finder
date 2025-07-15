// Main JavaScript for PG Finder

$(document).ready(function() {
    // Initialize tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();

    // Initialize popovers
    $('[data-bs-toggle="popover"]').popover();

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        $('.alert').fadeOut('slow');
    }, 5000);

    // Search form validation
    $('#searchForm').on('submit', function(e) {
        var city = $('#city').val();
        if (!city.trim()) {
            e.preventDefault();
            alert('Please select a city to search.');
            $('#city').focus();
        }
    });

    // Rating stars interaction
    $('.rating-input').on('click', function() {
        var rating = $(this).data('rating');
        var container = $(this).closest('.rating-container');

        container.find('.rating-input').each(function(index) {
            if (index < rating) {
                $(this).removeClass('far').addClass('fas');
            } else {
                $(this).removeClass('fas').addClass('far');
            }
        });

        container.find('input[name="rating"]').val(rating);
    });

    // Phone number formatting
    $('.phone-input').on('input', function() {
        var value = $(this).val().replace(/\D/g, '');
        if (value.length > 10) {
            value = value.substring(0, 10);
        }
        $(this).val(value);
    });

    // Price formatting
    $('.price-input').on('input', function() {
        var value = $(this).val().replace(/[^\d.]/g, '');
        $(this).val(value);
    });

    // Form submission loading state
    $('form').on('submit', function() {
        var submitBtn = $(this).find('button[type="submit"]');
        var originalText = submitBtn.text();
        submitBtn.prop('disabled', true).html('<span class="loading"></span> Loading...');

        // Re-enable button after 10 seconds (failsafe)
        setTimeout(function() {
            submitBtn.prop('disabled', false).text(originalText);
        }, 10000);
    });

    // Confirm delete actions
    $('.delete-btn').on('click', function(e) {
        if (!confirm('Are you sure you want to delete this item?')) {
            e.preventDefault();
        }
    });

    // Image preview for file uploads
    $('.image-upload').on('change', function() {
        var input = this;
        var preview = $(input).siblings('.image-preview');

        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                preview.attr('src', e.target.result).show();
            };
            reader.readAsDataURL(input.files[0]);
        }
    });

    // Smooth scrolling for anchor links
    $('a[href^="#"]').on('click', function(e) {
        e.preventDefault();
        var target = $($(this).attr('href'));
        if (target.length) {
            $('html, body').animate({
                scrollTop: target.offset().top - 70
            }, 500);
        }
    });

    // Search filters toggle (mobile)
    $('#filterToggle').on('click', function() {
        $('#searchFilters').toggleClass('show');
    });

    // Dynamic city loading
    $('#state').on('change', function() {
        var state = $(this).val();
        if (state) {
            // This would typically make an AJAX call to get cities
            // For now, we'll just clear the city field
            $('#city').val('').focus();
        }
    });

    // Facility checkboxes - limit selection
    $('.facility-checkbox').on('change', function() {
        var checked = $('.facility-checkbox:checked').length;
        if (checked > 5) {
            $(this).prop('checked', false);
            alert('You can select maximum 5 facilities.');
        }
    });

    // Contact form validation
    $('#contactForm').on('submit', function(e) {
        var email = $('#email').val();
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            e.preventDefault();
            alert('Please enter a valid email address.');
            $('#email').focus();
        }
    });

    // Price range slider (if using range inputs)
    $('.price-range').on('input', function() {
        var min = $('#minPrice').val();
        var max = $('#maxPrice').val();
        $('#priceRange').text('₹' + min + ' - ₹' + max);
    });

    // Auto-complete for city search (basic implementation)
    $('#citySearch').on('input', function() {
        var query = $(this).val();
        if (query.length > 2) {
            // This would typically make an AJAX call to get suggestions
            // For demo purposes, we'll show some static suggestions
            var suggestions = ['Bangalore', 'Mumbai', 'Delhi', 'Pune', 'Chennai', 'Hyderabad'];
            var filtered = suggestions.filter(city => 
                city.toLowerCase().includes(query.toLowerCase())
            );

            // Display suggestions (implement UI for this)
            console.log('Suggestions:', filtered);
        }
    });
});

// Utility functions
function formatCurrency(amount) {
    return '₹' + Number(amount).toLocaleString('en-IN');
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function showLoading(element) {
    $(element).html('<span class="loading"></span> Loading...');
}

function hideLoading(element, originalText) {
    $(element).html(originalText);
}

function showNotification(message, type = 'info') {
    var alertClass = 'alert-' + type;
    var alert = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    $('.container').first().prepend(alert);

    // Auto-hide after 5 seconds
    setTimeout(function() {
        $('.alert').first().fadeOut('slow');
    }, 5000);
}

// API functions
function fetchPGs(filters = {}) {
    return $.ajax({
        url: '/api/pgs',
        type: 'GET',
        data: filters,
        dataType: 'json'
    });
}

function bookPG(pgId, bookingData) {
    return $.ajax({
        url: `/api/book/${pgId}`,
        type: 'POST',
        data: JSON.stringify(bookingData),
        contentType: 'application/json',
        dataType: 'json'
    });
}

// Initialize map (if Google Maps is loaded)
function initMap() {
    if (typeof google !== 'undefined' && google.maps) {
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 13,
            center: {lat: 12.9716, lng: 77.5946} // Bangalore
        });

        // Add markers for PGs
        // This would be populated with actual PG data
    }
}

// Dark mode toggle (future feature)
function toggleDarkMode() {
    $('body').toggleClass('dark-mode');
    localStorage.setItem('darkMode', $('body').hasClass('dark-mode'));
}

// Load dark mode preference
$(document).ready(function() {
    if (localStorage.getItem('darkMode') === 'true') {
        $('body').addClass('dark-mode');
    }
});
