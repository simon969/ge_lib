ground_model_pile_set = {
    "ground_model": 
        {
        "description": "",
        "increment": -0.5,
        "set_names": [
            "_default"
        ],
        "strata": [
            {
                "sets": [
                    {
                        "cohesion": None,
                        "cu_grad": None,
                        "cu_top": None,
                        "density_dry": 18,
                        "density_sat": 20,
                        "description": "Made Ground (dry)",
                        "level_base": 100,
                        "level_top": 120,
                        "phi_deg": 32,
                        "set_name": "_default",
                        "thickness": 20,
                        "water_density": 10,
                        "water_level": 100,
                        "water_state": "dry"
                    }
                ]
            },
            {
                "sets": [
                    {
                        "cohesion": None,
                        "cu_grad": None,
                        "cu_top": None,
                        "density_dry": 18,
                        "density_sat": 20,
                        "description": "Made Ground (sat)",
                        "level_base": 98,
                        "level_top": 100,
                        "phi_deg": 32,
                        "set_name": "_default",
                        "thickness": 2,
                        "water_density": 10,
                        "water_level": 100,
                        "water_state": "unconfined"
                    }
                ]
            },
            {
                "sets": [
                    {
                        "cohesion": None,
                        "cu_grad": None,
                        "cu_top": 40,
                        "density_dry": 19,
                        "density_sat": 20,
                        "description": "Alluvium",
                        "level_base": 96,
                        "level_top": 98,
                        "phi_deg": 28,
                        "set_name": "_default",
                        "thickness": 2,
                        "water_density": 10,
                        "water_level": 98,
                        "water_state": "unconfined"
                    }
                ]
            },
            {
                "sets": [
                    {
                        "cohesion": None,
                        "cu_grad": None,
                        "cu_top": None,
                        "density_dry": 18,
                        "density_sat": 20,
                        "description": "River Terrace Deposist",
                        "level_base": 92,
                        "level_top": 96,
                        "phi_deg": 36,
                        "set_name": "_default",
                        "thickness": 4,
                        "water_density": 10,
                        "water_level": 98,
                        "water_state": "confined"
                    }
                ]
            },
            {
                "sets": [
                    {
                        "cohesion": 2,
                        "cu_grad": 8,
                        "cu_top": 70,
                        "density_dry": 20,
                        "density_sat": 20,
                        "description": "London Clay",
                        "level_base": 70,
                        "level_top": 92,
                        "phi_deg": 24,
                        "set_name": "_default",
                        "thickness": 22,
                        "water_density": 10,
                        "water_level": 98,
                        "water_state": "confined"
                    }
                ]
            }
        ],
        "strata_set": [
            {
                "cohesion": None,
                "cu_grad": None,
                "cu_top": None,
                "density_dry": 18,
                "density_sat": 20,
                "description": "Made Ground (dry)",
                "level_base": 100,
                "level_top": 120,
                "phi_deg": 32,
                "set_name": "_default",
                "thickness": 20,
                "water_density": 10,
                "water_level": 100,
                "water_state": "dry"
            },
            {
                "cohesion": None,
                "cu_grad": None,
                "cu_top": None,
                "density_dry": 18,
                "density_sat": 20,
                "description": "Made Ground (sat)",
                "level_base": 98,
                "level_top": 100,
                "phi_deg": 32,
                "set_name": "_default",
                "thickness": 2,
                "water_density": 10,
                "water_level": 100,
                "water_state": "unconfined"
            },
            {
                "cohesion": None,
                "cu_grad": None,
                "cu_top": 40,
                "density_dry": 19,
                "density_sat": 20,
                "description": "Alluvium",
                "level_base": 96,
                "level_top": 98,
                "phi_deg": 28,
                "set_name": "_default",
                "thickness": 2,
                "water_density": 10,
                "water_level": 98,
                "water_state": "unconfined"
            },
            {
                "cohesion": None,
                "cu_grad": None,
                "cu_top": None,
                "density_dry": 18,
                "density_sat": 20,
                "description": "River Terrace Deposist",
                "level_base": 92,
                "level_top": 96,
                "phi_deg": 36,
                "set_name": "_default",
                "thickness": 4,
                "water_density": 10,
                "water_level": 98,
                "water_state": "confined"
            },
            {
                "cohesion": 2,
                "cu_grad": 8,
                "cu_top": 70,
                "density_dry": 20,
                "density_sat": 20,
                "description": "London Clay",
                "level_base": 70,
                "level_top": 92,
                "phi_deg": 24,
                "set_name": "_default",
                "thickness": 22,
                "water_density": 10,
                "water_level": 98,
                "water_state": "confined"
            }
        ],
        "surcharge": 0,
        "water_density": 10
        },
    "pile_set": 
        {
        "description": "",
        "piles": [
            {
                "description": "450",
                "shape": "circular",
                "diameter": 0.45,
                "length": None,
                "breadth": None,
                "alpha": 0.6,
                "ks": 1,
                "tan_delta": 0.67,
                "nc": 9,
                "nq": 9.6,
                "calc_methods": "'qs_alpha_cu','qb_nc_cu','qs_ks_tandelta_po','qb_nq_po'",
                "pile_type": "cfa",
                "pile_test": "yes",
                "sls_check": "yes",
                "perimeter": 1.413716694115407,
                "base": 0.1590431280879833
            },
            {
                "description": "600",
                "shape": "circular",
                "diameter": 0.6,
                "length": None,
                "breadth": None,
                "alpha": 0.6,
                "ks": 1,
                "tan_delta": 0.67,
                "nc": 9,
                "nq": 9.6,
                "calc_methods": "'qs_alpha_cu','qb_nc_cu','qs_ks_tandelta_po','qb_nq_po'",
                "pile_type": "cfa",
                "pile_test": "yes",
                "sls_check": "yes",
                "perimeter": 1.8849555921538759,
                "base": 0.2827433388230814
            },
            {
                "description": "750",
                "shape": "circular",
                "diameter": 0.75,
                "length": None,
                "breadth": None,
                "alpha": 0.6,
                "ks": 1,
                "tan_delta": 0.67,
                "nc": 9,
                "nq": 9.6,
                "calc_methods": "'qs_alpha_cu','qb_nc_cu','qs_ks_tandelta_po','qb_nq_po'",
                "pile_type": "cfa",
                "pile_test": "yes",
                "sls_check": "yes",
                "perimeter": 2.356194490192345,
                "base": 0.44178646691106466
            },
            {
                "description": "900",
                "shape": "circular",
                "diameter": 0.9,
                "length": None,
                "breadth": None,
                "alpha": 0.6,
                "ks": 1,
                "tan_delta": 0.67,
                "nc": 9,
                "nq": 9.6,
                "calc_methods": "'qs_alpha_cu','qb_nc_cu','qs_ks_tandelta_po','qb_nq_po'",
                "pile_type": "cfa",
                "pile_test": "yes",
                "sls_check": "yes",
                "perimeter": 2.827433388230814,
                "base": 0.6361725123519332
            },
            {
                "description": "1050",
                "shape": "circular",
                "diameter": 1.05,
                "length": None,
                "breadth": None,
                "alpha": 0.6,
                "ks": 1,
                "tan_delta": 0.67,
                "nc": 9,
                "nq": 9.6,
                "calc_methods": "'qs_alpha_cu','qb_nc_cu','qs_ks_tandelta_po','qb_nq_po'",
                "pile_type": "cfa",
                "pile_test": "yes",
                "sls_check": "yes",
                "perimeter": 3.2986722862692828,
                "base": 0.8659014751456867
            },
            {
                "description": "1200",
                "shape": "circular",
                "diameter": 1.2,
                "length": None,
                "breadth": None,
                "alpha": 0.6,
                "ks": 1,
                "tan_delta": 0.67,
                "nc": 9,
                "nq": 9.6,
                "calc_methods": "'qs_alpha_cu','qb_nc_cu','qs_ks_tandelta_po','qb_nq_po'",
                "pile_type": "cfa",
                "pile_test": "yes",
                "sls_check": "yes",
                "perimeter": 3.7699111843077517,
                "base": 1.1309733552923256
            },
            {
                "description": "1000x750",
                "shape": "rectangular",
                "diameter": None,
                "length": 1,
                "breadth": 0.75,
                "alpha": 0.6,
                "ks": 1,
                "tan_delta": 0.67,
                "nc": 9,
                "nq": 9.6,
                "calc_methods": "'qs_alpha_cu','qb_nc_cu','qs_ks_tandelta_po','qb_nq_po'",
                "pile_type": "cfa",
                "pile_test": "yes",
                "sls_check": "yes",
                "perimeter": 3.5,
                "base": 0.75
            }
        ],
        "loadings": [
            {
                "description": "max vertical loading",
                "id": "001",
                "fx": 100,
                "fy": 100,
                "fz": 4000,
                "mx": 25,
                "my": 45,
                "mz": 10,
                "state": "uls_c2"
            },
            {
                "description": "max vertical loading",
                "id": "002",
                "fx": 100,
                "fy": 200,
                "fz": 3000,
                "mx": 25,
                "my": 45,
                "mz": 10,
                "state": "uls_c1"
            }
        ],
        "options": {
            "conc_density": 25,
            "methods": [
                "DrainedBearing_BS8004",
                "UndrainedBearing_BS8004",
                "DrainedBearing_EC7",
                "UndrainedBearing_EC7"
            ]
        }
        }
 
    }