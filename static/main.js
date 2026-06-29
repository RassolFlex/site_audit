console.log('init')

const audit_ssl_btn = document.querySelector('#audit_ssl')
const audit_cms_btn = document.querySelector('#audit_cms')
const audit_redirect_btn = document.querySelector('#audit_redirect')
const audit_domain_age_btn = document.querySelector('#audit_domain_age')
const audit_pagespeed_btn = document.querySelector('#audit_pagespeed')
const input_value = document.querySelector('#url')

audit_ssl_btn.addEventListener('click', (event) => {
    if (!input_value) return false
    let f = fetch('/api/v1/audit/ssl?url='+input_value.value)
    event.target.disabled = true
    f.then(response => {
        if (response.ok) {
            return response.json()
        };
    })
    .then(data => {
        console.log(data)
        if (data.ok) {
            document.querySelector('#has_ssl').textContent = 'Да'
            document.querySelector('#issuer').textContent = data.status.issuer
            document.querySelector('#days_left').textContent = data.status.not_after+' (осталось дней: '+data.status.days_left+')'
            document.querySelector('#domens').textContent = data.status.covers_all
            if (data.status.covers_www) {
                document.querySelector('#cover_www').textContent = 'Да'
            } else {
                document.querySelector('#cover_www').textContent = 'Нет'
            }
        } else {
            document.querySelector('#has_ssl').textContent = 'Нет'
            document.querySelector('#issuer').textContent = '-'
            document.querySelector('#days_left').textContent = '-'
            document.querySelector('#domens').textContent = '-'
            document.querySelector('#cover_www').textContent = '-'
        }
    })
    .finally(response => {
        event.target.disabled = false
    })
})

audit_cms_btn.addEventListener('click', (event) => {
    if (!input_value) return false
    let f = fetch('/api/v1/audit/cms?url='+input_value.value)
    event.target.disabled = true
    f.then(response => {
        if (response.ok) {
            return response.json()
        };
    })
    .then(data => {
        console.log(data)
        if (data.ok && data.cms) {
            document.querySelector('#has_cms').textContent = 'Да'
            document.querySelector('#cms_name').textContent = data.cms
        } else {
            document.querySelector('#has_cms').textContent = 'Нет'
            document.querySelector('#cms_name').textContent = '-'
        }
    })
    .finally(response => {
        event.target.disabled = false
    })
})

audit_redirect_btn.addEventListener('click', (event) => {
    if (!input_value) return false
    let f = fetch('/api/v1/audit/redirect?url='+input_value.value)
    event.target.disabled = true
    f.then(response => {
        if (response.ok) {
            return response.json()
        };
    })
    .then(data => {
        console.log(data)
        if (data.ok && data.has_www_redirect) {
            document.querySelector('#has_redirect').textContent = 'Да'
            document.querySelector('#redirects').textContent = data.redirect_chain
        } else {
            document.querySelector('#has_redirect').textContent = 'Нет'
            document.querySelector('#redirects').textContent = data.redirect_chain
        }
    })
    .finally(response => {
        event.target.disabled = false
    })
})


audit_domain_age_btn.addEventListener('click', (event) => {
    if (!input_value) return false
    let f = fetch('/api/v1/audit/domain_age?url='+input_value.value)
    event.target.disabled = true
    f.then(response => {
        if (response.ok) {
            return response.json()
        };
    })
    .then(data => {
        console.log(data)
        if (data.ok) {
            document.querySelector('#domain_age').textContent = data.age_years
            document.querySelector('#domain_registered').textContent = data.registered
            document.querySelector('#domain_registrar').textContent = data.registrar
        } else {
            document.querySelector('#domain_age').textContent = '-'
            document.querySelector('#domain_registered').textContent = '-'
            document.querySelector('#domain_registrar').textContent = '-'
        }
    })
    .finally(response => {
        event.target.disabled = false
    })
})


audit_pagespeed_btn.addEventListener('click', (event) => {
    if (!input_value) return false
    let f = fetch('/api/v1/audit/pagespeed?url='+input_value.value)
    event.target.disabled = true
    f.then(response => {
        if (response.ok) {
            return response.json()
        };
    })
    .then(data => {
        console.log(data)
        if (data.ok) {
            document.querySelector('#pagespeed_performance_score').textContent = data.performance_score+' / 100'
            document.querySelector('#pagespeed_FCP').textContent = data.FCP
            document.querySelector('#pagespeed_LCP').textContent = data.LCP
            document.querySelector('#pagespeed_TBT').textContent = data.TBT
            document.querySelector('#pagespeed_CLS').textContent = data.CLS
            document.querySelector('#pagespeed_SI').textContent = data.SI
        } else {
            document.querySelector('#pagespeed_performance_score').textContent = '-'
            document.querySelector('#pagespeed_FCP').textContent = '-'
            document.querySelector('#pagespeed_LCP').textContent = '-'
            document.querySelector('#pagespeed_TBT').textContent = '-'
            document.querySelector('#pagespeed_CLS').textContent = '-'
            document.querySelector('#pagespeed_SI').textContent = '-'
        }
    })
    .finally(response => {
        event.target.disabled = false
    })
})
