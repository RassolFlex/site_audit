console.log('init')

const audit_ssl_btn = document.querySelector('#audit_ssl')
const audit_cms_btn = document.querySelector('#audit_cms')
const audit_redirect_btn = document.querySelector('#audit_redirect')
const audit_domain_age_btn = document.querySelector('#audit_domain_age')
const audit_pagespeed_btn = document.querySelector('#audit_pagespeed')
const input_value = document.querySelector('#url')

async function runCheck(btn, endpoint, fillResults) {
    if (!input_value.value) {console.log('Введите адрес проверяемого сайта');return false}
    btn.disabled = true
    const btnText = btn.textContent
    btn.textContent = 'Идёт проверка...'
    try {
        const response = await fetch(`/api/v1/audit/${endpoint}?url=${input_value.value}`)
        const data = await response.json()
        fillResults(data)
    } finally {
        btn.disabled = false
        btn.textContent = btnText
    }
}

audit_ssl_btn.addEventListener('click', async (event) => {
    await runCheck(event.target, 'ssl', function(data) {
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
})

audit_cms_btn.addEventListener('click', async (event) => {
    await runCheck(event.target, 'cms', function(data) {
        if (data.ok && data.cms) {
            document.querySelector('#has_cms').textContent = 'Да'
            document.querySelector('#cms_name').textContent = data.cms
        } else {
            document.querySelector('#has_cms').textContent = 'Нет'
            document.querySelector('#cms_name').textContent = '-'
        }
    })
})

audit_redirect_btn.addEventListener('click', async (event) => {
    await runCheck(event.target, 'redirect', function(data) {
        if (data.ok && data.has_www_redirect) {
            document.querySelector('#has_redirect').textContent = 'Да'
            document.querySelector('#redirects').textContent = data.redirect_chain
        } else {
            document.querySelector('#has_redirect').textContent = 'Нет'
            document.querySelector('#redirects').textContent = data.redirect_chain
        }
    })
})


audit_domain_age_btn.addEventListener('click', async (event) => {
    await runCheck(event.target, 'domain_age', function(data) {
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
})


audit_pagespeed_btn.addEventListener('click', async (event) => {
    await runCheck(event.target, 'pagespeed', function(data) {
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
})
